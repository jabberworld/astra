#===istalismanplugin===
# -*- coding: utf-8 -*-

import html
import random
import re

import requests

NYA_HOME = 'https://nya.sh/'
NYA_POST = 'https://nya.sh/post/%s'
NYA_INFO = 'https://www.jabbrik.ru/info.txt'
NYA_TIMEOUT = 20
NYA_HEADERS = {'User-Agent': 'Mozilla/5.0'}


def nya_request(url):
        response = requests.get(url, headers=NYA_HEADERS, timeout=NYA_TIMEOUT)
        response.raise_for_status()
        response.encoding = response.encoding or 'windows-1251'
        return response.text


def decode(text):
        text = text.replace('<br />', '\n').replace('<br>', '\n')
        text = re.sub(r'<[^<>]+>', '', text)
        return html.unescape(text).replace('\t', '').replace('||||:]', '').replace('>[:\n', '').strip()


def post_ids(data):
        return re.findall(r'href=["\']/post/(\d+)', data)


def post_text(data):
        match = re.search(r'<div class=["\']content["\']>(.*?)</div>', data, re.S)
        return decode(match.group(1)) if match else ''


def get_post(post):
        try:
                data = nya_request(NYA_POST % int(post))
        except (requests.RequestException, ValueError):
                return ''
        return post_text(data)


def handler_nya_get(type, source, parameters):
        if parameters == u'инфо':
                try:
                        reply(type, source, nya_request(NYA_INFO))
                except requests.RequestException:
                        reply(type, source, u'Информация временно недоступна.')
                return
        try:
                if parameters:
                        post = int(parameters)
                        message = get_post(post)
                else:
                        home = nya_request(NYA_HOME)
                        posts = list(dict.fromkeys(post_ids(home)))
                        random.shuffle(posts)
                        post, message = None, ''
                        for candidate in posts:
                                message = get_post(candidate)
                                if message:
                                        post = candidate
                                        break
                if message:
                        reply(type, source, u'Цитата #%s:\n%s' % (post, message))
                else:
                        reply(type, source, u'Пост не найден.')
        except (requests.RequestException, ValueError):
                reply(type, source, u'Сервис цитат временно недоступен.')


register_command_handler(handler_nya_get, 'ня', ['фан', 'граббер', 'все'], 10,
                         'Показывает случайную цитату из НЯШа (nya.sh).\n (с) Gigabyte\nИдея: Тифлинг',
                         'ня', ['ня'])
