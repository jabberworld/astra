# BS mark.1
# /* coding: utf8 */
# BlackSmith Bot Plugin
# URL shortener using the u.to JSON API.

import requests

UTO_API = 'https://u.to/api/shorten/'
UTO_TIMEOUT = 20


def url_shortener(mType, source, args):
        if not args:
                reply(mType, source, u'Не нашёл URL.')
                return
        try:
                response = requests.post(
                        UTO_API,
                        json={'url': args.strip()},
                        timeout=UTO_TIMEOUT)
                response.raise_for_status()
                result = response.json()
                if result.get('success') and result.get('shortUrl'):
                        answer = result['shortUrl']
                else:
                        answer = u'Сервис не смог сократить ссылку.'
        except (requests.RequestException, ValueError) as error:
                answer = u'Ошибка сервиса сокращения ссылок: %s' % error
        reply(mType, source, answer)


command_handler(url_shortener, 11, 'uto-shortener')
