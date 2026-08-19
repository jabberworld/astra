# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  google_plugin.py

# (c) Gigabyte
# http://jabbrik.ru

import requests
import xml.etree.ElementTree as ET
        
def google(type, source, body):
        if body:
                try:
                        response = requests.get(
                                'https://www.bing.com/search',
                                params={'format': 'rss', 'q': body},
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=20)
                        response.raise_for_status()
                        item = ET.fromstring(response.content).find('./channel/item')
                        if item is None:
                                raise ValueError('no search results')
                        title = item.findtext('title', '').strip()
                        content = uHTML(item.findtext('description', '').strip())
                        url = item.findtext('link', '').strip()
                        text = '%s\n%s\n%s' % (title, content, url)
                        reply(type, source, text)
                except:
                        reply(type, source, u'Текст "%s" - не найден!' % (body))
        else:
                reply(type, source, u'Пустой запрос!')

command_handler(google, 10, "google")
