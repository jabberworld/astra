#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  kofe_plugin.py
#  Initial Copyright © 2010 Man (ManGust) man@jabberon.ru

KOFE = {u'каталог': u'''%s: список имеющихся кофе:
[1] espresso
[2] cappuccino (с молоком и пышной пенкой)
[3] glace (с мороженым)
[4] [Latte] Macchiato (с молочной пеной и кофе слоями)
[5] Mokko (с шоколадом)
[6] Ristretto (ароматный,бодрящий)
[7] Кофе с ванилью
[8] Кофе с корицей
[9] Кофе с ромом''',
                '1': u'приготовила кофе-espresso в специальной кофеварке, налила в кружечку, добавила 2 ложечки сахара и протянула - "%s"',
                '2': u'приготовила кофе-cappuccino с молоком и пышной пенкой, налила в кружечку, добавила 2 ложечки сахара и протянула - "%s"',
                '3': u'приготовила кофе-glace, налила в кружечку, добавила ст.ложку мороженого ,2 ложечки сахара и протянула - "%s"',
                '4': u'приготовила и налила в высокий бокал несмешанный капучино (Latte Macchiato), где молоко (3/4 части), молочная пена и кофе (1/4 части) лежат слоями, добавила 2 ложечки сахара и протянула бокал - "%s"',
                '5': u'приготовила кофе-Mokko, налила в кружечку, добавила шоколад и протянула - "%s"',
                '6': u'приготовила крепкий, бодрящий, ароматный  кофе-Ristretto, налила в кружечку, (без сахара) и протянула - "%s"',
        '7': u'приготовила кофе, добавила ваниль и две ложечки сахара и протянула - "%s"',
        '8': u'приготовила черный кофе, добавила корицу и протянула ароматный напиток - "%s"',
        '9': u'приготовила черный кофе, добавила ром и протянула бодрящий напиток - "%s"'}

def handler_kofe(type, source, parameters):
        if type == 'private':
                reply(type, source, u'пиши в групчат')
                return
        
        groupchat = source[1]
        publ = 0
        priv = 1

        if not groupchat in GROUPCHATS:
                reply(type, source, u'только для конференций!')
                return

        prms = parameters.split(' ', 1)

        if len(prms ) == 2:
                kofe_key = prms[0]
                nick = prms[1]
                
        elif len(prms ) == 1:
                kofe_key = prms[0]
                nick = source[2]
                
        else:
                reply(type, source, u'для получения списка кофе наберите "кофе каталог"')
                return
        if nick in GROUPCHATS[groupchat].keys():
                if kofe_key in KOFE and GROUPCHATS[groupchat][nick]['ishere']:
                        res = '/me %s' % (KOFE[kofe_key] % nick)
                        msg(groupchat, res)
                
                else: 
                        reply(type,source,u'для получения списка кофе наберите "кофе каталог"')
                        return
        else:
                reply(type,source,u'нет здесь такого ника')
                                
register_command_handler(handler_kofe, 'кофе', ['все','никто'], 10, 'kofe_plugin \nответ на слово кофе','приготовление разных видов кофе\nцифры 1-6 - это выбор какой кофе будет налит ботом\nby Man (ManGust)', ['кофе','кофе каталог','кофе 2','кофе 2 Man (налить кофе "2" пользователю - Man)'])
