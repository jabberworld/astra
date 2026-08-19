# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
import re
import json
import traceback
from urllib.request import quote

Langs = {'en': u'Английский',
                        'ja': u'Японский',
                        'ru': u'Русский',
                        'auto': u'Авто',
                        'sq': u'Албанский',
                        'ar': u'Арабский',
                        'af': u'Африкаанс',
                        'be': u'Белорусский',
                        'bg': u'Болгарский',
                        'cy': u'Валлийский',
                        'hu': u'Венгерский',
                        'vi': u'Вьетнамский',
                        'gl': u'Галисийский',
                        'el': u'Греческий',
                        'nl': u'Голландский',
                        'da': u'Датский',
                        'iw': u'Иврит',
                        'yi': u'Идиш',
                        'id': u'Индонезийский',
                        'ga': u'Ирландский',
                        'is': u'Исландский',
                        'es': u'Испанский',
                        'it': u'Итальянский',
                        'kk': u'Казахский',
                        'ca': u'Каталанский',
                        'zh-CN': u'Китайский',
                        'ko': u'Корейский',
                        'la': u'Латинский',
                        'lv': u'Латышский',
                        'lt': u'Литовский',
                        'mk': u'Македонский',
                        'ms': u'Малайский',
                        'mt': u'мальтийский',
                        'de': u'Немецкий',
                        'no': u'Норвежский',
                        'fa': u'Персидский',
                        'pl': u'Польский',
                        'pt': u'Португальский',
                        'ro': u'Румынский',
                         'sr': u'Сербский',
                         'sk': u'Словацкий',
                         'sl': u'Словенский',
                         'sw': u'Суахили',
                         'tl': u'Тагальский',
                        'tg': u'Таджикский',
                         'th': u'Тайский',
                         'tr': u'Турецкий',
                         'uk': u'Украинский',
                         'fi': u'Финский',
                         'fr': u'Французский',
                         'hi': u'Хинди',
                         'hr': u'Хорватский',
                         'cs': u'Чешский',
                         'sv': u'Шведский',
                         'et': u'Эстонский'}

AGENT_CHROME = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"



def gTrans(sl, tl, q):
        url = "http://translate.googleapis.com/translate_a/single?client=gtx&sl=%s&tl=%s&dt=t&q=%s"
        text = quote(q)
        js = read_url(url % (sl,tl,text), AGENT_CHROME)
        js = json.loads(js)[0]
        result = ""
        for key in js:
                item = key[0]
                if item:
                        result += item + " "
        result = result.strip()
        return result

def gAutoTrans(mType, source, text):
        try:
                if text:
                        repl = gTrans("auto", "ru", text)
                        if text == repl:
                                #repl = u"Перевод %s => %s:\n%s" % ("auto", "en", gTrans("auto", "en", text))
                                repl = u"Автоперевод на Английский:\n%s" % gTrans("auto", "en", text)
                        else:
                                #repl = u"Перевод %s => %s:\n%s" % ("auto", "ru", repl)
                                repl = u"Автоперевод на Русский:\n%s" % repl
                else:
                        repl = u"Недостаточно параметров."
        except:
                repl = u"Ошибка в параметрах. Смотри помощь по команде"
        reply(mType, source, repl)

def gTransHandler(mType, source, args):
        if args and len(args.split()) > 2:
                (fLang, tLang, text) = args.split(None, 2)
                try:
                        msgtext = u"Перевод c %s на %s:\n%s" % (Langs[fLang], Langs[tLang], gTrans(fLang, tLang, text))
                except:
                        msgtext = u"Ошибка в параметрах. Смотри помощь по команде!"
                reply(mType, source, msgtext)
        else:
                answer = u"\nДоступные языки:\n"
                for a, b in enumerate(sorted([x + u" — " + y for x, y in Langs.items()])):
                        answer += u"%i. %s.\n" % (a + 1, b)
                reply(mType, source, answer.encode("utf-8"))

command_handler(gTransHandler, 10, "trans")
command_handler(gAutoTrans, 10, "trans")
