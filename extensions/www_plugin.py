#===istalismanplugin===
# -*- coding: utf-8 -*-

import requests
from html import unescape

def hnd_www(type, source, parameters):
    if not parameters:
        return
    if not parameters.count('.'):
        reply(type, source, u'Неверный адрес!')
        return
    try:
        page=''
        url = parameters if parameters.startswith(('http://', 'https://')) else 'https://' + parameters
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        response.raise_for_status()
        data = response.text
        data = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', data)
        data = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', data)
        if data.count('</style>'):
            data = ''.join(data.split('style')[2:])
        page = re.compile(r'<[^<>]*>').sub('', data)
        page = unescape(page).replace('\n\n','').replace('&nbsp;','').replace('&gt;','')
        page = '\n'.join([x for x in page.splitlines() if not x.isspace()])
        #page = ''.join(map(lambda x: x.strip(), page.splitlines()))
        reply(type, source, page)
    except:
        traceback.print_exc()
        reply(type, source, u'Ошибочка!')

register_command_handler(hnd_www, 'www', ['все'], 10, 'Получить содержимое веб страницы', 'www url', ['www mail.ru'])
