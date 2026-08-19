#===istalismanplugin===
# -*- coding: utf-8 -*-
import re
import requests

# автор - ferym@jabbim.org.ru
# по вопросам обращаться в support@conference.veganet.org.ru
# web site: http://veganet.org
# plugin version 1.0

REFERAT_URLS = {
        u'астрономия': 'http://referats.yandex.ru/astronomy.xml',
        u'геология': 'http://referats.yandex.ru/geology.xml',
        u'гироскопия': 'http://referats.yandex.ru/gyroscope.xml',
        u'литература': 'http://referats.yandex.ru/literature.xml',
        u'маркетинг': 'http://referats.yandex.ru/marketing.xml',
        u'математика': 'http://referats.yandex.ru/mathematics.xml',
        u'музыка': 'http://referats.yandex.ru/music.xml',
        u'политология': 'http://referats.yandex.ru/polit.xml',
        u'почвоведение': 'http://referats.yandex.ru/agrobiologia.xml',
        u'правоведение': 'http://referats.yandex.ru/law.xml',
        u'психология': 'http://referats.yandex.ru/psychology.xml',
        u'география': 'http://referats.yandex.ru/geography.xml',
        u'физика': 'http://referats.yandex.ru/physics.xml',
        u'философия': 'http://referats.yandex.ru/philosophy.xml',
        u'химия': 'http://referats.yandex.ru/chemistry.xml',
        u'эстетика': 'http://referats.yandex.ru/estetica.xml',
}

def decode_referat(text):
        return stripTags(text.replace('<br />', '\n').replace('<br>', '\n')
                        .replace('</h1>', '\n\n').replace('<p>', '').replace('</p>', ''))

def handler_refer(type, source, parameters):
        if not parameters:
                reply(type, source, u'выберите категорию реферата!\nподробнее "помощь реферат"')
                return
        if parameters == u'категории':
                categ = sorted(REFERAT_URLS.keys())
                repl = (u'Доступны рефераты по следующим категориям:\n' + u',\n'.join(categ)
                        + u'\nВсего (' + str(len(categ)) + u') категорий.\n'
                        + u'Что бы сгенерировать реферат по определённой категории, '
                        + u'выполните команду "реферат <категория>\nby ferym"')
                reply(type, source, repl)
                return
        url = REFERAT_URLS.get(parameters.strip().lower())
        if not url:
                reply(type, source, u'Не существующая категория!\nподробнее "помощь реферат"')
                return
        try:
                proxies = {'http': WEATHER_PROXY, 'https': WEATHER_PROXY} if WEATHER_PROXY else None
                r = requests.get(url, headers={'User-Agent': UserAgents['Firefox']},
                                 proxies=proxies, timeout=WEATHER_TIMEOUT)
                target = r.content.decode('cp1251', 'replace')
                od = re.search('<h1 style="color:black; margin-left:0;">', target)
                if not od:
                        reply(type, source, u'Возможно сменили разметку')
                        return
                message = target[od.end():]
                stop = re.search('</div></td>', message)
                if stop:
                        message = message[:stop.start()]
                message = '\n' + decode_referat(message).strip()
                if type == 'private':
                        reply(type, source, message)
                else:
                        reply(type, source, u'ушло в приват')
                        reply('private', source, message)
        except Exception:
                reply(type, source, u'не могу получить реферат, сервис недоступен')

register_command_handler(handler_refer, 'реферат', ['mod','все'], 10,'Генерация рефератов по выбранным вами темам.\nДля просмотра доступных категорий выполните команду "реферат категории"','реферат <категория>', ['реферат философия','реферат категории\nby ferym\nplugin version 1.0'])