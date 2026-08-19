#===istalismanplugin===
# -*- coding: utf-8 -*-

import re
from urllib.parse import urlencode
from urllib.request import urlopen


STIHI_URL = 'https://www.stihi.ru/cgi-bin/assist.pl'
STIHI_HEADERS = {'User-Agent': 'Mozilla/5.0'}


def stihi_request(fields):
        data = urlencode(fields).encode('utf-8')
        response = urlopen(STIHI_URL, data=data, timeout=20)
        return response.read().decode('windows-1251', 'replace')


def open_rif(type, source, parameters):
        if not parameters:
                reply(type, source, u'к какому слову мне искать рифмы?')
                return
        words = parameters.strip().split()
        if len(words) == 1:
                try:
                        data = stihi_request({'word': parameters[:100]})
                        if data.count('<li>') >= 1:
                                start = re.search('<ul>', data).end()
                                data = data[start:re.search('</table>', data[start:]).start() + start]
                                data = data.replace('<li>', '').replace('</li>', '').replace('</ul></td><td valign="top"><ul>', '').replace('</ul>', '').replace('</td>', '').replace('</tr>', '')
                                values = data.replace('\n\n', '\n').split('\n')
                                text = ', '.join(values).strip()
                                text = text[3:len(text) - 1]
                                reply(type, source, u'Рифмы к слову "%s": %s' % (parameters, text))
                        else:
                                reply(type, source, u'Рифмы к слову "%s" не найдены' % parameters)
                except Exception:
                        reply(type, source, u'кажется что-то сломалось')
                return
        try:
                data = stihi_request({'newstrings': parameters[:100]})
                if len(data.split('\n')) == 1 and data.count('<select name=') >= 1:
                        values = re.findall(r'<option value=.*?>(.*?)</option>', data, re.S)
                        reply(type, source, u'Рифмы к фразе "%s": %s' % (parameters, '; '.join(values)))
                elif data.count('<textarea cols="60" rows="5" name="strings" wrap="virtual" class="textassist">'):
                        marker = '<textarea cols="60" rows="5" name="strings" wrap="virtual" class="textassist">'
                        text = data.split(marker, 1)[1].split('</textarea>', 1)[0].strip()
                        reply(type, source, u'Рифмы к четверостишью:\n%s' % text)
                else:
                        reply(type, source, u'Рифмы к фразе "%s" не найдены' % parameters)
        except Exception:
                reply(type, source, u'кажется что-то сломалось')


register_command_handler(open_rif, 'рифма', ['все'], 10, 'показывает рифму к словам, фразам, стихам', 'рифма <слово\фраза\стих>', ['рифма пиво'])
