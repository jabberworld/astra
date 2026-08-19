# BS mark.1-55
# /* coding: utf-8 */

import re
from urllib.parse import quote

def search_sonnik(text, type):
        try:
                text = quote(text.strip())
                data = read_url('http://signorina.ru/services/sonnik/?target=%s&field=1' % text, UserAgents['Firefox']).replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
        except:
                return u'Не возможно получить данные'
        title = re.findall(r'class="result"><br />[^<]+', data)
        if title:
                return_text = u''
                for i in range(len(title)):
                        title_f = title[i][24:]
                        return_text += '%s\n' % title_f
                        if type != 'private' and i == 5:
                                break
                return return_text[:-1]
        else:
                return u'Ничего не найдено'

def handler_sonnik(type, source, body):
        if body:
                reply(type, source, search_sonnik(body, type))
        else:
                reply(type, source, u'Что искать?')

command_handler(handler_sonnik, 10, "sonnik")
