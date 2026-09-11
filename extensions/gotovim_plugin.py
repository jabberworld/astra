#===istalismanplugin===
# -*- coding: utf-8 -*-

# by Evgеn (xmpp:allertvitter@conference.qip.ru)

import re
import requests

def open_gotovim(type,source,parameters):
        try:
                proxies = {'http': NETWORK_PROXY, 'https': NETWORK_PROXY} if NETWORK_PROXY else None
                req = requests.get("http://www.gotovim.ru/recepts/random.shtml",
                                   headers={'User-Agent': UserAgents['Firefox']},
                                   proxies=proxies, timeout=NETWORK_TIMEOUT)
                data = req.content.decode('cp1251', 'replace')
                if data.count('<h1>')>=1:
                        od = re.search('<h1>',data)
                        h2 = data[od.end():]
                        h1 = h2[:re.search('</h1>',h2).start()]
                        od = re.search('<td><h3>',h2)
                        h2 = h2[od.end():]
                        h3 = h2[:re.search('</h3>',h2).start()]
                        h1=h1+u'\n'+h3+u'\n\n'
                        od = re.search('<ul class="recipeList">',h2)
                        h2 = h2[od.end():]
                        h3 = h2[:re.search('</td>',h2).start()]
                        h3=h3.replace('<li>', '-').replace('  ', ' ').replace('</div>', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('<br>', '\n')
                        h1=h1+h3+u'\n'
                        od = re.search('<p class=dsc>',h2)
                        h2 = h2[od.end():]
                        h3 = h2[:re.search('</p>',h2).start()]
                        h3=h3.replace('<p class=dsc>', ' ')
                        h1=h1+h3
                        reply(type,source, h1)
                else:
                        reply(type,source, u'Возможно сменили разметку')
        except:
                reply(type,source,u'кажется что-то сломалось')

register_command_handler(open_gotovim, 'рецепт', ['все'], 10, 'показывает случайный рецепт с http://www.gotovim.ru/recepts/random.shtml', 'рецепт', ['рецепт'])