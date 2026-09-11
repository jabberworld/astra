# BS mark.1-55
# /* coding: utf-8 */

###
import logging
logging.captureWarnings(True)
from urllib.parse import quote, unquote
###

WIKI_RESULTS = {}
WIKI_MAX_RESULTS = 5
WIKI_URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search=[SEARCH]&prop=info&inprop=url&format=json'

def wiki_get_result(source, flag):
        data = WIKI_RESULTS.get('%s/%s' % (source[1],source[2]))
        if data:
                text = []
                while True:
                        if len(data) > 0:
                                i = data.pop(0)
                                if flag == True:
                                        text.append('%s\n%s\n%s' % (i[0], i[1], i[2]))
                                else:
                                        text.append('%s\n%s' % (i[0], i[2]))
                                if len(text) > WIKI_MAX_RESULTS - 1:
                                        break
                        else:
                                break
                text = u'Найдено:\n' + '\n'.join(text)
                if len(data) > 0:
                        text += '\nЕще %i по команде "вики далее" либо "вики * далее"' % len(data)
                WIKI_RESULTS['%s/%s' % (source[1],source[2])] = data
                return text
        else:
                return

def wiki_search(source, body, flag):
        data = read_url(WIKI_URL.replace('[SEARCH]', quote(body)), 'Mozilla/5.0')
        if data:
                result = []
                data = simplejson.loads(data)
                for i in range(len(data[1])):
                        title = data[1][i]
                        text = data[2][i]
                        link = unquote(data[3][i]).replace(' ', '%20')
                        result.append((title, text, link))
                WIKI_RESULTS['%s/%s' % (source[1],source[2])] = result
                if len(result) == 1:
                        return wiki_get_result(source, True)
                else:
                        return wiki_get_result(source, flag)
        else:
                return

def handler_wiki(type, source, body):
        if body:
                if body.startswith('* '):
                        if body[2:].lower() == 'далее':
                                text = wiki_get_result(source, True)
                                if not text:
                                        text = u'Далее пусто'
                        else:
                                text = wiki_search(source, body[2:], True)
                elif body.lower() == 'далее':
                        text = wiki_get_result(source, False)
                        if not text:
                                text = u'Далее пусто'
                else:
                        text = wiki_search(source, body, False)
                if text:
                        if type != 'private' and len(text) > 700:
                                reply(type, source, u'Величина текста %i символ(а), отсылаю в приват' % len(text))
                                reply('private', source, text)
                        else:
                                reply(type, source, text)
                else:
                        reply(type, source, u'Поиск не дал результатов')
        else:
                reply(type, source, u'Что искать?')

command_handler(handler_wiki, 10, "wiki")
