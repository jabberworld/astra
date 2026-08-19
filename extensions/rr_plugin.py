#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  roulette_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007-2008 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import os, shutil


"""
1ая осечка - 1
2ая осечка - 3
3ая осечка - 5
4ая осечка - 7
5ая осечка - 9
6ая осечка - 11
выстрел - 0
"""
RR_ACTIVE = {}
RR_BARABAN = {} # [0,0,1,0,0,0]
#                  1 2 3 4 5 6
USERS = {}

# User bases
RR_GLOBAL_BD = {}
RR_LOCAL_BD = {}

#RR_GLOBAL_BD = {u'gigabyte@jabbrik.ru': {'detail': {'bonus': 0, 'score': 0}, 'statistic': {'2st': 1, '5st': 0, '6st': 0, 'shots': 5, '1st': 1, 'deads': 1, '3st': 1, '4st': 1}}}
#RR_LOCAL_BD = {u'stalker@conference.jabbrik.ru': {u'gigabyte@jabbrik.ru': {'detail': {'bonus': 0, 'score': 0}, 'statistic': {'2st': 1, '5st': 0, '6st': 0, 'shots': 5, '1st': 1, 'deads': 1, '3st': 1, '4st': 1}}}}

# ----------
RR_ONLINE = {}
"""
RR_REPLIC = {1:[u'И-так, первая осечка', u'Редко конечно когда с первого разу прям бух', u'Одно очко этот храбрец уже заработал'],
             2:[u'Вторая осечка! Кто знает может сейчас будет выстрел?', u'Если честно мне кажеться что это была последняя осечка', u'Три очка!'],
             3:[u'В барабане всего шесть патронов, сейчас пять - пустые, это уже третья осечка!!', u'Третья осечка даёт 5 очков в карман счастливцу'],
             4:[u'Напряжение растет! Редко кто до этого доживал, в любом случае он свои 7 очков получит', u'Очень страшно... я вся на нервах'],
             5:[u'Оченб напряженная ситуация!'],
             6:[u'Дааааа!!! Это нереально но факт!', u'Шестая осечка! А знаете что это значит? Заведомо можно прощаться с следущим участником', u'Везуха! 11 очков'],
             0:[u'Это была игра сильных, но не всё так плохо']
             }
"""

RR_REPLIC = {1:[u'И-так, первая осечка', u'Редко конечно когда с первого разу прям бух', u'Одно очко этот храбрец уже заработал'],
 2:[u'Вторая осечка! Кто знает может сейчас будет выстрел?', u'Если честно мне кажеться что это была последняя осечка', u'Три очка!'],
 3:[u'Ах да... забыла предупредить, в барабане всего семь патронов, шесть - пустые, один заряжен, это уже третья осечка!!', u'Третья осечка даёт 5 очков в карман счастливцу'],
 4:[u'Напряжение растет! Редко кто до этого доживал, в любом случае он свои 7 очков получит', u'Четвертая осечка!!!', u'Очень страшно... я вся на нервах'],
 5:[u'Ох ну и игра, на лицах игроков виден азарт!', u'Нет!!!! Ну вы видели это??? Пятая осечка!!!', u'Доктора мне!!! 9 очков в банке!'],
 6:[u'Дааааа!!! Это нереально но факт!', u'Шестая осечка! А знаете что это значит? Заведомо можно прощаться с следущим участником', u'Везуха! Шире карман открой, 11 очков с тобой!'],
 0:[u'Это была игра сильных, но не всё так плохо', u'Аста ла виста Бэйби']
 }

def rr_reg(t, s, b):
        global RR_ACTIVE
        JID = handler_jid(s[0])
        if not s[1] in RR_ACTIVE.keys():
                RR_ACTIVE[s[1]] = {}

        if not JID in RR_ACTIVE[s[1]].keys():
                if len(RR_ACTIVE)<7:
                        if len(RR_ACTIVE[s[1]]) == 0:
                                RR_ACTIVE[s[1]][JID] = {'nick':s[2], 'owner':1, 'now':0, 'game':1}
                        else:
                                RR_ACTIVE[s[1]][JID] = {'nick':s[2], 'owner':0, 'now':0, 'game':1}
                        msg(s[1], s[2]+': '+u'Вы вступили в смертельную игру.')
                else:
                        msg(s[1], s[2]+': '+u'Играть одновременно может не более семи человек комнаты')
        else:
                msg(s[1], s[2]+': '+u'Вы и так в игре')

def rr_rand_drum(conf):
        global RR_BARABAN
        RR_BARABAN[conf] = []
        patrons = 1
        a = []
        a = random.randrange(0, 7)
        for i in range(0, 7):
                if i == a:
                        RR_BARABAN[conf].append(1)
                else:
                        RR_BARABAN[conf].append(0)
        return 1

def rr_rand_users(conf):
        USERS[conf] = []
        while 1:
                u = random.choice(list(RR_ACTIVE[conf].keys()))
                if not u in USERS[conf]:
                        USERS[conf].append(u)
                if len(USERS[conf])>=len( RR_ACTIVE[conf].keys() ):
                        break
        return 1

def rr_proccess(s):
        u = USERS[s][0]
        p = RR_BARABAN[s][0]
        
        USERS[s] = rr_route( USERS[s] )
        RR_BARABAN[s] = rr_route( RR_BARABAN[s] )

        RR_ACTIVE[s][ u ]['now'] = 0
        RR_ACTIVE[s][ USERS[s][0] ]['now'] = 1

        return [u, p]

def rr_route(mas):
    b = []
    for j, i in enumerate(mas):
        if j == 0:
            aa = i
        else:
            b.append(i)
    else:
        b.append(aa)
    return b

def rr_start(t, s, b):
        global RR_ONLINE
        if not s[1] in RR_ACTIVE:
                reply(t, s, u'Необходим хотя бы один участник')
                return
        if len(RR_ACTIVE)==0:
                reply(t, s, u'Необходим хотя бы один участник')
                return
        JID = handler_jid(s[0])

        RR_ONLINE[s[1]] = {}
        RR_ONLINE[s[1]]['num'] = 0
        rr_rand_drum(s[1])
        rr_rand_users(s[1])
        if JID in RR_ACTIVE[s[1]]:
                a = RR_ACTIVE[s[1]][JID]['owner']
        else:
                a = 0
        
        if (a == 1) or has_access(s[0], 20, s[1]):
                for i in RR_ACTIVE[s[1]]:
                        RR_ACTIVE[s[1]][ i ]['now'] = 0
                RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['now'] = 1
                
                msg(s[1], u'Игра начата в количестве %i участников, я передаю пистолет участнику %s и жду когда он спустит курок (команда рр)' % (len(USERS[s[1]]), RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['nick'] ) )
        else:
                msg(s[1], s[2]+': '+u'Запустить игру может только её хозяин!')

def rr_restart(s):
        global RR_ONLINE
        JID = handler_jid(s[0])
        rr_rand_drum(s[1])
        rr_rand_users(s[1])
        RR_ONLINE[s[1]]['num'] = 0
        for i in RR_ACTIVE[s[1]]:
                RR_ACTIVE[s[1]][ i ]['now'] = 0
        RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['now'] = 1
                
        msg(s[1], u'Я снова зарядила барабан, нас %i участников, я передаю пистолет участнику %s и жду когда он спустит курок (команда рр)' % (len(USERS[s[1]]), RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['nick'] ) )




def rr_check(t, s, b):
        global RR_ONLINE
        if not s[1] in RR_ACTIVE:
                reply(t, s, u'Необходим хотя бы один участник')
                return

        if len(RR_ACTIVE[s[1]])==0:
                reply(t, s, u'Необходим хотя бы один участник')
                return
        if not s[1] in RR_ONLINE:
                reply(t, s, u'Запусти игру')
                return
        JID = handler_jid(s[0])

        if not JID in RR_ACTIVE[s[1]]:
                reply(t, s, u'Тебя нет в списке играющих')
                return

        RR_ONLINE[s[1]]['num'] += 1

        if RR_ACTIVE[s[1]][ JID ]['now'] == 1:
                a = rr_proccess(s[1])
                if a[0] == JID:
                        if a[1] == 1:
                                msg(s[1], u'Птыдыщь! Раздался выстрел в %s. %s' % (s[2], random.choice( RR_REPLIC[0] ) ) )
                                rr_add_score(s[1], JID, '0st')
                                for i in RR_ACTIVE[s[1]]:
                                        if i == JID:
                                                rr_save_score(s[1], JID, 1)
                                        else:
                                                rr_save_score(s[1], JID, 0)
                                rr_save_base()
                                del RR_TMP[s[1]]
                                time.sleep(1)
                                rr_restart(s)
                        else:
                                if RR_ONLINE[s[1]]['num'] == 1:
                                        rr_add_score(s[1], JID, '1st')
                                elif RR_ONLINE[s[1]]['num'] == 2:
                                        rr_add_score(s[1], JID, '2st')
                                elif RR_ONLINE[s[1]]['num'] == 3:
                                        rr_add_score(s[1], JID, '3st')
                                elif RR_ONLINE[s[1]]['num'] == 4:
                                        rr_add_score(s[1], JID, '4st')
                                elif RR_ONLINE[s[1]]['num'] == 5:
                                        rr_add_score(s[1], JID, '5st')
                                elif RR_ONLINE[s[1]]['num'] == 6:
                                        rr_add_score(s[1], JID, '6st')

                                msg(s[1], s[2]+': '+u'Щёлк! Осечка! %s Следущим стреляет %s' % ( random.choice(RR_REPLIC[RR_ONLINE[s[1]]['num']]) , RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['nick'] ))
                else:
                        msg(s[1], s[2]+': '+u'Техошибка. Обратитесь к администратору бота. Игра остановлена. Приношу извинения за неудобства.')
                        del RR_ACTIVE[s[1]]
                        del RR_BARABAN[s[1]]
                        del RR_ONLINE[s[1]]
        else:
                msg(s[1], s[2]+': '+u'Сейчас не ваш ход, ожидается выстрел %s' % (RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['nick']))

def rr_unreg(t, s, b):
        global RR_ACTIVE
        JID = handler_jid(s[0])
        if s[1] in RR_ACTIVE.keys():
                if JID in RR_ACTIVE[s[1]].keys():

                        if JID in USERS[s[1]]:
                                i = USERS[s[1]].index( JID )
                                if i == 0:
                                        del USERS[s[1]][i]
                                        if len(USERS[s[1]]) == 0:
                                                msg(s[1], s[2]+': '+u'Участников не осталось, игра остановлена')
                                                del RR_ACTIVE[s[1]]
                                                del RR_BARABAN[s[1]]
                                                del RR_ONLINE[s[1]]
                                                return
                                        RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['now'] = 1
                                        msg(s[1], u'Внимание!: '+u'У участника %s сдали нервы, он выходит из игры теряя всё что заработал за этот период а право выстрел апереходит к %s' % (RR_ACTIVE[s[1]][ JID ]['nick'], RR_ACTIVE[s[1]][ USERS[s[1]][0] ]['nick']) )
                                        del RR_ACTIVE[s[1]][JID]
                                else:
                                        del USERS[s[1]][i]
                                        del RR_ACTIVE[s[1]][JID]
                                        msg(s[1], s[2]+': '+u'Вы вышли')
                else:
                        msg(s[1], s[2]+': '+u'Вероятно вы уже вышли.')
        else:
                msg(s[1], s[2]+': '+u'Игра не создана чтобы из нее выходить)))')

def rr_stop(t, s, b):

        JID = handler_jid(s[0])

        if not s[1] in RR_ACTIVE:
                msg(s[1], s[2]+': '+u'Нет игры')
                return
        
        if JID in RR_ACTIVE[s[1]]:
                a = RR_ACTIVE[s[1]][JID]['owner']
        else:
                a = 0
        
        if (a == 1) or has_access(s[0], 20, s[1]):
                del RR_ACTIVE[s[1]]
                del RR_BARABAN[s[1]]
                del RR_ONLINE[s[1]]
                msg(s[1], s[2]+': '+u'Игра остановлена')
        else:
                msg(s[1], s[2]+': '+u'Только хозяин игры или красный может остановить её!')
RR_TMP = {}
def rr_add_score(conf, jid, type=''):
        global RR_TMP
        if not conf in RR_TMP:
                RR_TMP[conf] = {}
        if not jid in RR_TMP[conf]:
                RR_TMP[conf][jid] = {'statistic':{},
                                     'detail':{}
                                     }
                RR_TMP[conf][jid]['statistic'] = {'shots':0, # всего выстрелов
                                                     'deads':0, # всего смертей
                                                     '1st':0, # осечка первого уровня
                                                     '2st':0, # осечка второго уровня
                                                     '3st':0, # осечка третьего уровня
                                                     '4st':0, # осечка четвертого уровня
                                                     '5st':0, # осечка пятого уровня
                                                     '6st':0,
                                                     }
                RR_TMP[conf][jid]['detail'] = {'score':0,
                                               'bonus':0, # за 6st - 50pts, за 5st - 40pts, за 4st - 30pts
                                               }
        
        RR_TMP[conf][jid]['statistic']['shots'] +=1
        if type == '1st':
                RR_TMP[conf][jid]['statistic']['1st'] +=1
                RR_TMP[conf][jid]['detail']['score'] +=1
        elif type == '2st':
                RR_TMP[conf][jid]['statistic']['2st'] +=1
                RR_TMP[conf][jid]['detail']['score'] +=3
        elif type == '3st':
                RR_TMP[conf][jid]['statistic']['3st'] +=1
                RR_TMP[conf][jid]['detail']['score'] +=5
        elif type == '4st':
                RR_TMP[conf][jid]['statistic']['4st'] +=1
                RR_TMP[conf][jid]['detail']['bonus'] +=30
                RR_TMP[conf][jid]['detail']['score'] +=7
        elif type == '5st':
                RR_TMP[conf][jid]['statistic']['5st'] +=1
                RR_TMP[conf][jid]['detail']['bonus'] +=40
                RR_TMP[conf][jid]['detail']['score'] +=9
        elif type == '6st':
                RR_TMP[conf][jid]['statistic']['6st'] +=1
                RR_TMP[conf][jid]['detail']['bonus'] +=50
                RR_TMP[conf][jid]['detail']['score'] +=11
        elif type == '0st':
                RR_TMP[conf][jid]['statistic']['deads'] +=1
                RR_TMP[conf][jid]['detail']['score'] +=0

#        print RR_TMP
 #       print RR_GLOBAL_BD
#        print RR_LOCAL_BD

def rr_save_score(conf, jid, dead):
        global RR_LOCAL_BD
        global RR_GLOBAL_BD
        if not conf in RR_LOCAL_BD:
                RR_LOCAL_BD[conf] = {}
        if not jid in RR_LOCAL_BD[conf]:
                RR_LOCAL_BD[conf][jid] =  {'statistic':{'shots':0, # всего выстрелов
                                                     'deads':0, # всего смертей
                                                     '1st':0, # осечка первого уровня
                                                     '2st':0, # осечка второго уровня
                                                     '3st':0, # осечка третьего уровня
                                                     '4st':0, # осечка четвертого уровня
                                                     '5st':0, # осечка пятого уровня
                                                     '6st':0,
                                                     },
                                           'detail':{'score':0,
                                               'bonus':0, # за 5st - 50pts, за 4st - 40pts, за 30st - 30pts
                                               }
                                           }
        
        if not jid in RR_GLOBAL_BD:
                RR_GLOBAL_BD[jid] =  {'statistic':{'shots':0, # всего выстрелов
                                                     'deads':0, # всего смертей
                                                     '1st':0, # осечка первого уровня
                                                     '2st':0, # осечка второго уровня
                                                     '3st':0, # осечка третьего уровня
                                                     '4st':0, # осечка четвертого уровня
                                                     '5st':0, # осечка пятого уровня
                                                     '6st':0,
                                                     },
                                      'detail':{'score':0,
                                               'bonus':0, # за 5st - 50pts, за 4st - 40pts, за 30st - 30pts
                                               }
                                      }

        if dead:
                RR_LOCAL_BD[conf][jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                RR_LOCAL_BD[conf][jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                RR_LOCAL_BD[conf][jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                RR_LOCAL_BD[conf][jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                RR_LOCAL_BD[conf][jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                RR_LOCAL_BD[conf][jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                RR_LOCAL_BD[conf][jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']
                RR_LOCAL_BD[conf][jid]['statistic']['6st'] += RR_TMP[conf][jid]['statistic']['6st']

                RR_GLOBAL_BD[jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                RR_GLOBAL_BD[jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                RR_GLOBAL_BD[jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                RR_GLOBAL_BD[jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                RR_GLOBAL_BD[jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                RR_GLOBAL_BD[jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                RR_GLOBAL_BD[jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']
                RR_GLOBAL_BD[jid]['statistic']['6st'] += RR_TMP[conf][jid]['statistic']['6st']
        else:
                RR_LOCAL_BD[conf][jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                RR_LOCAL_BD[conf][jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                RR_LOCAL_BD[conf][jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                RR_LOCAL_BD[conf][jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                RR_LOCAL_BD[conf][jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                RR_LOCAL_BD[conf][jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                RR_LOCAL_BD[conf][jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']
                RR_LOCAL_BD[conf][jid]['statistic']['6st'] += RR_TMP[conf][jid]['statistic']['6st']

                RR_GLOBAL_BD[jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                RR_GLOBAL_BD[jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                RR_GLOBAL_BD[jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                RR_GLOBAL_BD[jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                RR_GLOBAL_BD[jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                RR_GLOBAL_BD[jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                RR_GLOBAL_BD[jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']
                RR_GLOBAL_BD[jid]['statistic']['6st'] += RR_TMP[conf][jid]['statistic']['6st']


                RR_LOCAL_BD[conf][jid]['detail']['score'] += RR_TMP[conf][jid]['detail']['score']
                RR_LOCAL_BD[conf][jid]['detail']['bonus'] += RR_TMP[conf][jid]['detail']['bonus']

                RR_GLOBAL_BD[jid]['detail']['score'] += RR_TMP[conf][jid]['detail']['score']
                RR_GLOBAL_BD[jid]['detail']['bonus'] += RR_TMP[conf][jid]['detail']['bonus']
        

#        print RR_TMP
#        print RR_GLOBAL_BD
#        print RR_LOCAL_BD

"""
        else:
                if not conf in RR_LOCAL_BD:
                        RR_LOCAL_BD[conf] = {}
                if not jid in RR_LOCAL_BD[conf]:
                        RR_LOCAL_BD[conf][jid] =  {'statistic':{}, 'detail':{}}
                
                if not jid in RR_GLOBAL_BD:
                        RR_GLOBAL_BD[jid] =  {'statistic':{}, 'detail':{}}

                if type=='0st':
                        RR_LOCAL_BD[conf][jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                        RR_LOCAL_BD[conf][jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                        RR_LOCAL_BD[conf][jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                        RR_LOCAL_BD[conf][jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                        RR_LOCAL_BD[conf][jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                        RR_LOCAL_BD[conf][jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                        RR_LOCAL_BD[conf][jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']

                        RR_GLOBAL_BD[jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                        RR_GLOBAL_BD[jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                        RR_GLOBAL_BD[jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                        RR_GLOBAL_BD[jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                        RR_GLOBAL_BD[jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                        RR_GLOBAL_BD[jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                        RR_GLOBAL_BD[jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']
                else:
                        RR_LOCAL_BD[conf][jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                        RR_LOCAL_BD[conf][jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                        RR_LOCAL_BD[conf][jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                        RR_LOCAL_BD[conf][jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                        RR_LOCAL_BD[conf][jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                        RR_LOCAL_BD[conf][jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                        RR_LOCAL_BD[conf][jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']

                        RR_GLOBAL_BD[jid]['statistic']['shots'] += RR_TMP[conf][jid]['statistic']['shots']
                        RR_GLOBAL_BD[jid]['statistic']['deads'] += RR_TMP[conf][jid]['statistic']['deads']
                        RR_GLOBAL_BD[jid]['statistic']['1st'] += RR_TMP[conf][jid]['statistic']['1st']
                        RR_GLOBAL_BD[jid]['statistic']['2st'] += RR_TMP[conf][jid]['statistic']['2st']
                        RR_GLOBAL_BD[jid]['statistic']['3st'] += RR_TMP[conf][jid]['statistic']['3st']
                        RR_GLOBAL_BD[jid]['statistic']['4st'] += RR_TMP[conf][jid]['statistic']['4st']
                        RR_GLOBAL_BD[jid]['statistic']['5st'] += RR_TMP[conf][jid]['statistic']['5st']


                        RR_LOCAL_BD[conf][jid]['detail']['score'] += RR_TMP[conf][jid]['detail']['score']
                        RR_LOCAL_BD[conf][jid]['detail']['bonus'] += RR_TMP[conf][jid]['detail']['bonus']

                        RR_GLOBAL_BD[jid]['detail']['score'] += RR_TMP[conf][jid]['detail']['score']
                        RR_GLOBAL_BD[jid]['detail']['bonus'] += RR_TMP[conf][jid]['detail']['bonus']

        print(RR_TMP)
        print(RR_GLOBAL_BD)
        print(RR_LOCAL_BD)

"""


def rr_get_score(t, s, b):
        O = u'[%nick - локальная статистика]\nБаллы/бонусы: %score/%bonus\nВыстрелы: %shots\nПровалы: %dead\nСтатистика: %st'
        O1 = u'[%nick - глобальная статистика]\nБаллы/бонусы: %score/%bonus\nВыстрелы: %shots\nПровалы: %dead\nСтатистика: %st'
        a = ''

        if not b:
                JID = handler_jid(s[0])
                NICK = s[2]
        else:
                if b in GROUPCHATS[s[1]]:
                        JID = handler_jid(s[1]+'/'+b)
                        NICK = b
                else:
                        msg(s[1], u'Нет таких тут')
                        return
        
        if s[1] in RR_LOCAL_BD:
                if JID in RR_LOCAL_BD[ s[1] ]:
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['1st'])+'/'
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['2st'])+'/'
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['3st'])+'/'
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['4st'])+'/'
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['5st'])+'/'
                        a+=str(RR_LOCAL_BD[s[1]][JID]['statistic']['6st'])
                        o = O.replace('%dead', str(RR_LOCAL_BD[s[1]][JID]['statistic']['deads']) ).replace('%st', a).replace('%nick', NICK).replace('%score', str(RR_LOCAL_BD[s[1]][JID]['detail']['score']) ).replace('%bonus', str(RR_LOCAL_BD[s[1]][JID]['detail']['bonus']) ).replace('%shots', str(RR_LOCAL_BD[s[1]][JID]['statistic']['shots']) )
                        msg(s[1], o)
                else:
                        msg(s[1], u'Для %s нет локальной статистики' % (NICK))
        else:
                msg(s[1], u'Нет этой комнаты в статистике ваще')

def rr_get_score_global(t, s, b):
        O = u'[%nick - локальная статистика]\nБаллы/бонусы: %score/%bonus\nВыстрелы: %shots\nПровалы: %dead\nСтатистика: %st'
        O1 = u'[%nick - глобальная статистика]\nБаллы/бонусы: %score/%bonus\nВыстрелы: %shots\nПровалы: %dead\nСтатистика: %st'
        a = ''

        if not b:
                JID = handler_jid(s[0])
                NICK = s[2]
        else:
                if b in GROUPCHATS[s[1]]:
                        JID = handler_jid(s[1]+'/'+b)
                        NICK = b
                else:
                        msg(s[1], u'Нет таких тут')
                        return
        
        if JID in RR_GLOBAL_BD:
                b+=str(RR_GLOBAL_BD[JID]['statistic']['1st'])+'/'
                b+=str(RR_GLOBAL_BD[JID]['statistic']['2st'])+'/'
                b+=str(RR_GLOBAL_BD[JID]['statistic']['3st'])+'/'
                b+=str(RR_GLOBAL_BD[JID]['statistic']['4st'])+'/'
                b+=str(RR_GLOBAL_BD[JID]['statistic']['5st'])+'/'
                b+=str(RR_GLOBAL_BD[JID]['statistic']['6st'])
                o = O1.replace('%dead', str(RR_GLOBAL_BD[JID]['statistic']['deads']) ).replace('%st', b).replace('%nick', NICK).replace('%score', str(RR_GLOBAL_BD[JID]['detail']['score']) ).replace('%bonus', str(RR_GLOBAL_BD[JID]['detail']['bonus']) ).replace('%shots', str(RR_GLOBAL_BD[JID]['statistic']['shots']) )
                msg(s[1], o)
        else:
                msg(s[1], u'Для %s нет глобальной статистики' % (NICK))




def rr_save_base():
        global RR_LOCAL_BD
        global RR_GLOBAL_BD
        B = {'RR_GLOBAL_BD':RR_GLOBAL_BD,
             'RR_LOCAL_BD':RR_LOCAL_BD
             }
        if os.path.exists('dynamic/RR.txt'):
                try:
                        fp = open('dynamic/RR.txt', 'r')
                        tmp = eval(fp.read())
                        fp.close()
                        
                        if os.path.exists('dynamic/RR_bak.txt'):
                                os.remove('dynamic/RR_bak.txt')
                        shutil.copy('dynamic/RR.txt','dynamic/RR_bak.txt')
#                        print 'Save backup'
                except:
                        pass
#                        os.remove('dynamic/RR.txt')
#                        print 'Del base'

        fp = open('dynamic/RR.txt', 'w')
        fp.write(str(B))
        fp.close()

def rr_load_base():
        global RR_GLOBAL_BD
        global RR_LOCAL_BD
        
        B = {'RR_GLOBAL_BD':RR_GLOBAL_BD,
             'RR_LOCAL_BD':RR_LOCAL_BD
             }
        try:
                fp = open('dynamic/RR.txt', 'r')
                tmp = eval(fp.read())
                fp.close()
                RR_GLOBAL_BD = tmp['RR_GLOBAL_BD']
                RR_LOCAL_BD = tmp['RR_LOCAL_BD']
#                print 'Load normal'
        except:
                try:
                        fp = open('dynamic/RR_bak.txt', 'r')
                        tmp = eval(fp.read())
                        fp.close()
                        RR_GLOBAL_BD = tmp['RR_GLOBAL_BD']
                        RR_LOCAL_BD = tmp['RR_LOCAL_BD']
#                        print 'Load backup'
                except:
                        RR_GLOBAL_BD = {}
                        RR_LOCAL_BD = {}
#                        print 'Load default base'


def rr_help(t, s, b):
        reply(t, s,"""
РР - Русская Рулетка - наиболее бездумная игра для бота, бездумная не в смысле тупая, а всмысле что думать особо не надо, всё в руках матушки фартуны.
Правила необычайно просты, игрой управляют 7 команд (пока что), сейчас подробнее о них:
1. rr_reg - регистрация игрока, посути это значит ваше согласие на игру и подтверждение того, что вам есть +18 лет. Синтаксиса команда не имеет, просто rr_reg, зато есть ограничения на количество одновременно играющих - 7 (по количеству патронов в барабане револьвера)
2. rr_unreg - команда обратная предыдущей rr_reg - выход из игры, при её использовании очки теряются заработанные в цикле.
3. rr_start - запуск игры с зарегистрировшимися игроками. Выполнить повторно для пересоздания цикла или для того чтобы впустить вновь пришедших. P.S. выполняется автоматом аосле каждого цикла.
4. rr_stop - остановка игры.
5. rr_stat - статистика игры для себя или другого ника (в параметре к команде) для этой комнаты. Для более подробной информации см. приложение №1
6. rr_gstat - статистика игры для себя или другого ника (в параметре к команде) для всех комнат. Для более подробной информации см. приложение №1
7. рр - англ. или русск. буквы, собственно сам выстрел (естественно в себя)

Игра происходит по циклам, один цикл это 6 тактов (максимум), количество тактов определяет положение патрона в барабане. Такты называются так:
1st - первый так, 2st второй, 3st третий, 4st четвертый, 5st пятый, 6st шестой и 0st это выстрел в голову, этакий полутакт.

---Приложение №1---
при получении статистики пользователя мы видим нечто подобное:
Баллы/бонусы: 167/90
Выстрелы: 33
Провалы: 7
Статистика: 12/15/9/3/1/1

БАЛЛЫ это ваши очки за игру, начисляются следущим способом: чем выше ваш такт тем больше баллов, 1-3-5-7-9-11 баллов соответственно за 1ый, 2ой, 3ий, 4ый, 5ый и 6ой такт. Если игрок провалился, то очки и бонусы сгорают.
БОНУСЫ это баллы за сверх-игру, даются за 4ый, 5ый и 6ой такты 30, 40 и 50 соответственно.
ВЫСТРЕЛЫ это ваше количество выстрелов. Не сгорает при неудаче.
ПРОВАЛЫ количетсво ваших "смертей", не сгорает))
СТАТИСТИКА - это количество побитых тактов, первое число это первый такт, второе - второй и т.д. В нашем примере это 12 первых тактов, 15 вторых и т.д.

- - - - - - - -
На будущее конечно же наполеоновские планы, это и возврат к возможности кика за выстрел, и игра на выбывание и др, но пока это тут вот как есть и вроде работает <]
""")



register_command_handler(rr_get_score_global, 'рргстат', ['рр','все'], 10, 'Выстрелить.', 'рр (русские буквы)', ['рр'])
register_command_handler(rr_get_score, 'ррстат', ['рр','все'], 10, 'Выстрелить.', 'рр (русские буквы)', ['рр'])
register_command_handler(rr_check, 'рр', ['рр','все'], 10, 'Выстрелить.', 'рр (русские буквы или английские буквы)', ['рр'])
register_command_handler(rr_check, 'pp', ['рр','все'], 10, 'Выстрелить.', 'рр (русские буквы или английские буквы)', ['pp'])
register_command_handler(rr_reg, 'рррег', ['рр','все'], 10, 'Регистрация в игре. Участник попадает в игру только после перезапуска игры', 'рррег', ['рррег'])
register_command_handler(rr_start, 'ррстарт', ['рр','все'], 10, 'Запуск игры в русскую рулетку', 'ррстарт', ['ррстарт'])
register_command_handler(rr_unreg, 'ррарег', ['рр','все'], 10, 'Выйти из игры.', 'ррарег', ['ррарег'])
register_command_handler(rr_stop, 'ррстоп', ['рр','все'], 10, 'Остановка игры в русскую рулетку', 'ррстоп', ['ррстоп'])
register_command_handler(rr_help, 'ррпомощь', ['игры','все'], 10, 'Помощь', 'ррпомощь', ['ррпомощь'])
