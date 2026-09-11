# BS mark.1-55
# /* coding: utf-8 */

import json
import logging
from html.parser import HTMLParser
from urllib.parse import quote

import requests

logging.captureWarnings(True)

search_gis = 'https://www.gismeteo.ru/api/v2/search/searchresultforsuggest/'
url_gis = 'http://m.gismeteo.ru/weather/[ID]/detailday/[DAY]/'
url_gis_current = 'https://www.gismeteo.ru[URL]now/'
useragent = 'OperaMini'
weather_headers = {'User-Agent': UserAgents[useragent]}
gis_days = {'0': 'сегодня', '1': 'завтра', '2': 'послезавтра'}


def weather_request(url, save_response=False):
        proxies = {'http': NETWORK_PROXY, 'https': NETWORK_PROXY} if NETWORK_PROXY else None
        response = requests.get(url, headers=weather_headers, proxies=proxies, timeout=NETWORK_TIMEOUT)
        response.raise_for_status()
        data = response.text
        if save_response:
                write_file(WEATHER_RESPONSE_FILE, data)
        return data


def get_id_gis(body):
        try:
                data = weather_request(search_gis + quote(body))
                content = json.loads(data)
                if content.get('total', 0) <= 0:
                        return None, None, None, None
                item = content['items'][0]
                country = ''
                if item.get('district'):
                        country += '%s, ' % item['district'].get('name')
                if item.get('country'):
                        country += item['country'].get('name') or ''
                country = country.replace(', None', '').replace('None', '')
                return str(item['id']), item['name'], item['url'], '(' + country + ')'
        except Exception:
                return None, None, None, None


class WeatherParser(HTMLParser):
        def __init__(self):
                HTMLParser.__init__(self, convert_charrefs=True)
                self.temperatures = []
                self.speeds = []
                self.pressures = []
                self.metrics = {}
                self.description = []
                self.timestamp = None
                self.sun = {}
                self.stack = []
                self.title_buffer = []
                self.value_buffer = []
                self.measure_buffer = []
                self.current_title = None
                self.active_title = False
                self.active_value = False
                self.active_measure = False
                self.active_description = False
                self.pending_sun_timestamp = None

        def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                classes = set((attrs.get('class') or '').split())
                self.stack.append((tag, classes))
                if tag == 'temperature-value' and attrs.get('value') is not None:
                        self.temperatures.append(attrs['value'].replace('&minus;', '-'))
                        if self.active_value:
                                self.value_buffer.append(attrs['value'].replace('&minus;', '-'))
                elif tag == 'speed-value' and attrs.get('value') is not None:
                        self.speeds.append(attrs['value'])
                        if self.active_value:
                                self.value_buffer.append(attrs['value'])
                elif tag == 'pressure-value' and attrs.get('value') is not None:
                        self.pressures.append(attrs['value'])
                        if self.active_value:
                                self.value_buffer.append(attrs['value'])
                elif tag == 'time-value':
                        if 'now-localdate' in classes:
                                self.timestamp = attrs.get('timestamp')
                        elif 'time' in classes:
                                self.pending_sun_timestamp = attrs.get('timestamp')
                if 'now-desc' in classes:
                        self.active_description = True
                elif 'item-title' in classes:
                        self.title_buffer = []
                        self.active_title = True
                elif 'item-value' in classes:
                        self.value_buffer = []
                        self.active_value = True
                elif 'item-measure' in classes:
                        self.measure_buffer = []
                        self.active_measure = True

        def handle_endtag(self, tag):
                _, classes = self.stack.pop() if self.stack else (tag, set())
                if 'now-desc' in classes:
                        self.active_description = False
                elif 'item-title' in classes:
                        self.active_title = False
                        self.current_title = ''.join(self.title_buffer).strip()
                elif 'item-value' in classes:
                        self.active_value = False
                        if self.current_title:
                                self.metrics[self.current_title] = (
                                        ''.join(self.value_buffer).strip(),
                                        self.metrics.get(self.current_title, (None, ''))[1])
                elif 'item-measure' in classes:
                        self.active_measure = False
                        if self.current_title in self.metrics:
                                value = self.metrics[self.current_title][0]
                                self.metrics[self.current_title] = (
                                        value, ''.join(self.measure_buffer).strip())

        def handle_data(self, data):
                text = ' '.join(data.split())
                if not text:
                        return
                if self.active_description:
                        self.description.append(text)
                elif self.active_title:
                        self.title_buffer.append(text)
                elif self.active_value:
                        self.value_buffer.append(text)
                elif self.active_measure:
                        self.measure_buffer.append(text)
                if self.pending_sun_timestamp and self.stack and 'caption' in self.stack[-1][1]:
                        self.sun[text.lower()] = self.pending_sun_timestamp
                        self.pending_sun_timestamp = None

        def result(self):
                def metric(name):
                        return self.metrics.get(name, (None, None))

                wind = metric('Ветер')
                date = None
                if self.timestamp:
                        date = time.strftime('%d.%m.%Y %H:%M', time.localtime(int(self.timestamp)))
                return (
                        date,
                        self.temperatures[0] if self.temperatures else None,
                        self.temperatures[1] if len(self.temperatures) > 1 else None,
                        self.speeds[0] if self.speeds else wind[0],
                        wind[1],
                        self.pressures[0] if self.pressures else None,
                        metric('Влажность')[0],
                        metric('Вода')[0] or (self.temperatures[2] if len(self.temperatures) > 2 else None),
                        metric('Г/м')[0],
                        time.strftime('%H:%M', time.localtime(int(self.sun['восход']))) if self.sun.get('восход') else None,
                        time.strftime('%H:%M', time.localtime(int(self.sun['заход']))) if self.sun.get('заход') else None,
                        None, None, None, None,
                        ' '.join(self.description) or None)


def parse_state(data):
        marker = 'window.M.state = '
        try:
                start = data.index(marker) + len(marker)
                return json.JSONDecoder().raw_decode(data[start:])[0]
        except (ValueError, json.JSONDecodeError):
                return {}


def parse_temp(data):
        parser = WeatherParser()
        parser.feed(data)
        parser.close()
        return parser.result()


def get_gis(body, day):
        city_id, name, url, country = get_id_gis(body)
        if not city_id:
                return u'Не найдено'
        try:
                if day == -1:
                        raw_data = weather_request(url_gis_current.replace('[URL]', url), save_response=True)
                        state = parse_state(raw_data)
                        city_data = state.get('city', {}).get('translations', {}).get('ru', {}).get('city', {})
                        name = city_data.get('name') or name
                        data = parse_temp(raw_data)
                        text = ('%s %s:\nДанные на: %s\nТемпература: %s C, '
                                'По ощущению: %s C\nВетер: %s м/с, %s\n'
                                'Давление: %s мм, Влажность: %s%%\nВода: %s C, '
                                'Г/м активность: %s балл(ов)\nСолнце: восход %s, '
                                'заход %s\n%s\n%s\n%s' %
                                (name, country, data[0], data[1], data[2], data[3],
                                 data[4], data[5], data[6], data[7], data[8],
                                 data[9], data[10], data[11], data[12], data[13]))
                        return text.replace('\nNone', '')
                raw_data = weather_request(url_gis.replace('[ID]', city_id).replace('[DAY]', str(day)), save_response=True)
                data = parse_temp(raw_data)
                return ('%s %s на %s:\n[%s]\n%s %s\n%s\n%s\n%s' %
                        (name, country, gis_days[day], data[0], data[1], data[2],
                         data[3], data[4], data[5]))
        except Exception:
                return u'Ошибка при обработке данных'


def parse_body(body):
        parts = body.strip().lower().split(' ', 1)
        if len(parts) == 1:
                return parts[0], -1
        if parts[0] in gis_days:
                return parts[1], parts[0]
        return ' '.join(parts), -1


def command_gis(type, source, body):
        if body:
                city, day = parse_body(body)
                reply(type, source, get_gis(city, day) if city else u'Введены не корректные данные')
        else:
                reply(type, source, u'Там точно нет погоды')


command_handler(command_gis, 10, 'weather')
