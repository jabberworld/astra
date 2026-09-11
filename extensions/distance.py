# BS mark.1-55
# /* coding: utf-8 */

from urllib.parse import quote

distance_url = "http://www.avtodispetcher.ru/distance/export/frame?from=%(args1)s&to=%(args2)s"

text = u'''Расстояние между %s и %s составляет %sкм. Время в пути: %s
Общий расход топлива легкового авто (10л/100км): %dл., а так же грузового авто(35л/100км): %dл
Общие завтраты на бензин (45руб/л.) легкового авто: %dруб., а так же грузового авто : %dруб. Так же общие завтраты на газ (22руб/л.) легкового авто: %dруб.'''

def command_distance(mType, source, body):
        if body:
                args = body.split()
                if len(args) == 2:
                        town1, town2 = (str(x) for x in args)
                        args1, args2 = (quote(str(x)) for x in args)
                        data = read_url(distance_url % vars(), UserAgents["Firefox"])
                        try:
                                total = re.search(r'totalDistance">[^<]+', data, 16).group()[15:]
                                time = re.search(r'totalTime">[^<]+', data, 16).group()[11:]
                                fl = 10.0 / 100.0 * float(total)
                                fg = 45.0 / 100.0 * float(total)
                                zl = 45 * int(fl)
                                zg = 45 * int(fg)
                                zh = 22 * int(fl)
                                data = text % (town1, town2, total, time, fl, fg, zl, zg, zh)
                                reply(mType, source, data)
                        except:
                                reply(mType, source, u'Что-то не так...')
                elif len(args) > 2:
                        reply(mType, source, u'Название городов состоящие из двух или более слов пишите слитно либо разделите _')

command_handler(command_distance, 11, "distance")
