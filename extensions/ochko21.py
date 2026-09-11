#===istalismanplugin===
# -*- coding: utf-8 -*-

# Initial Copyright © 2010 Evgеn. Меня можно найти в конференци xmpp:allertvitter@conference.qip.ru, на сайте http://40tman.ucoz.ru, http://witcher-team.ucoz.ru


ochko21 = [u'6_крести',u'7_крести',u'8_крести',u'9_крести',u'10_крести',u'валет_крести',u'дама_крести',u'кароль_крести',u'туз_крести',u'6_пики',u'7_пики',u'8_пики',u'9_пики',u'10_пики',u'валет_пики',u'дама_пики',u'кароль_пики',u'туз_пики',u'6_черви',u'7_черви',u'8_черви',u'9_черви',u'10_черви',u'валет_черви',u'дама_черви',u'кароль_черви',u'туз_черви',u'6_буби',u'7_буби',u'8_буби',u'9_буби',u'10_буби',u'валет_буби',u'дама_буби',u'кароль_буби',u'туз_буби']
ochko21_q = {}

def ochko21_start(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        if source[1] in ochko21_q:
                reply(type,source, u'в данную игру уже играют, подождите 3 минуты.')
                return
        groupchat = source[1]
        nick=source[2]
        jid=handler_jid(groupchat+'/'+nick)
        e = u'Вы начали игру в 21 очко. Для раздачи вам карты напишите "карту", для окончания игры напишите "хватит", если наберете "вдвоем ник", то можно в данную игру играть вдвоем'
        k = random.randrange(0, 9999)
        ochko21_q[groupchat] = {}
        ochko21_q[groupchat][jid]={'ochko21': 0, 'ochki': 0, 'karta1': u'0', 'karta2': u'0', 'karta3': u'0', 'karta4': u'0', 'karta5': u'0', 'karta6': u'0', 'karta7': u'0', 'karta8': u'0', 'karta9': u'0', 'karta10': u'0', 'xod': 0, 'xod1': 0, 'jid3': u'0', 'xod2': 0, 'nick1': nick, 'stop': k}
        reply(type,source, e)
        ochko21_stop(type, source, jid, k)

def ochko21_stop(type, source, jid, k):
        groupchat = source[1]
        nick=source[2]
        time.sleep(180)
        if groupchat in ochko21_q:
                if jid in ochko21_q[groupchat] and nick in GROUPCHATS[groupchat] and ochko21_q[groupchat][jid]['stop'] == k:
                        reply(type,source,u'3 минуты истекли, игра закончена.')
                        del  ochko21_q[groupchat]
                
def ochko21_msg(HREN,type,source,parameters):
        groupchat = source[1]
        nick=source[2]
        if groupchat not in GROUPCHATS:
                return
        jid=handler_jid(groupchat+'/'+nick)
        if not groupchat in ochko21_q:
                return
        if jid in ochko21_q[groupchat]:
                parameters=parameters.strip()
                parameters2=parameters.split()
                if ochko21_q[groupchat][jid]['xod']==0:
                        if ochko21_q[groupchat][jid]['xod2']==0:
                                if parameters2[0] == u'вдвоем':
                                        if ochko21_q[groupchat][jid]['xod1']>=1:
                                                reply(type,source,u'в игре могут участвовать только 2 игрока')
                                                return
                                        ochko21_q[groupchat][jid]['xod1'] = 1
                                        ochko21_q[groupchat][jid]['xod2'] = 2
                                        if parameters2[1] in GROUPCHATS[groupchat]:
                                                jid2=handler_jid(groupchat+'/'+parameters2[1])
                                                ochko21_q[groupchat][jid]['jid3'] = jid2
                                                ochko21_q[groupchat][jid2]={'ochko21': 0, 'ochki': 0, 'karta1': u'0', 'karta2': u'0', 'karta3': u'0', 'karta4': u'0', 'karta5': u'0', 'karta6': u'0', 'karta7': u'0', 'karta8': u'0', 'karta9': u'0', 'karta10': u'0', 'xod': 0, 'xod1': 2, 'jid3': jid, 'xod2': 1, 'nick1': parameters2[1]}
                                                reply(type,source, parameters2[1]+u' присоединяется к игре, '+source[2]+u', для раздачи вам карты напишите "карту"')
                if ochko21_q[groupchat][jid]['xod2'] == 2:
                        if ochko21_q[groupchat][jid]['xod']==0 or ochko21_q[groupchat][jid]['xod']==2 or ochko21_q[groupchat][jid]['xod']==4 or ochko21_q[groupchat][jid]['xod']==6 or ochko21_q[groupchat][jid]['xod']==8 or ochko21_q[groupchat][jid]['xod']==10 or ochko21_q[groupchat][jid]['xod']==12: 
                                if parameters == u'карту':
                                        ochko21_q[groupchat][jid]['xod'] = ochko21_q[groupchat][jid]['xod'] + 1
                                        hh = random.choice(ochko21)
                                        ochko21_q[groupchat][jid]['ochko21'] = ochko21_q[groupchat][jid]['ochko21'] + 1
                                        if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                                hh = random.choice(ochko21)
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh == u'6_крести' or hh == u'6_пики':
                                                k = 6
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'6_черви' or hh == u'6_буби':
                                                k = 6
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'7_крести' or hh == u'7_пики' or hh == u'7_черви' or hh == u'7_буби':
                                                k = 7
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'8_крести' or hh == u'8_пики' or hh == u'8_черви' or hh == u'8_буби':
                                                k = 8
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'9_крести' or hh == u'9_пики' or hh == u'9_черви' or hh == u'9_буби':
                                                k = 9
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'10_крести' or hh == u'10_пики' or hh == u'10_черви' or hh == u'10_буби':
                                                k = 10
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'валет_крести' or hh == u'валет_пики' or hh == u'валет_черви' or hh == u'валет_буби':
                                                k = 2
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'дама_крести' or hh == u'дама_пики' or hh == u'дама_черви' or hh == u'дама_буби':
                                                k = 3
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'кароль_крести' or hh == u'кароль_пики' or hh == u'кароль_черви' or hh == u'кароль_буби':
                                                k = 4
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'туз_крести' or hh == u'туз_пики' or hh == u'туз_черви' or hh == u'туз_буби':
                                                k = 11
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if ochko21_q[groupchat][jid]['ochko21']==1:
                                                ochko21_q[groupchat][jid]['karta1'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==3:
                                                ochko21_q[groupchat][jid]['karta2'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==5:
                                                ochko21_q[groupchat][jid]['karta3'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==7:
                                                ochko21_q[groupchat][jid]['karta4'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==9:
                                                ochko21_q[groupchat][jid]['karta5'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==11:
                                                ochko21_q[groupchat][jid]['karta6'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==13:
                                                ochko21_q[groupchat][jid]['karta7'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==15:
                                                ochko21_q[groupchat][jid]['karta8'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==17:
                                                ochko21_q[groupchat][jid]['karta9'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==19:
                                                ochko21_q[groupchat][jid]['karta10'] = hh
                                        if ochko21_q[groupchat][jid]['ochki'] > 21:
                                                asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                                reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf+u' очков. Вы проиграли!')
                                                ochko21_q[groupchat][jid]['xod1'] = 5
                                                ochko21_q[groupchat][jid]['xod2'] = 3
                                                wet = ochko21_q[groupchat][jid]['jid3']
                                                ochko21_q[groupchat][wet]['xod1'] = 0
                                                ochko21_q[groupchat][wet]['xod2'] = 3
                                                nick1 = ochko21_q[groupchat][wet]['nick1']
                                                msg(groupchat, nick1+u': ваш ход')
                                                return
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf)
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        ochko21_q[groupchat][wet]['xod'] = ochko21_q[groupchat][wet]['xod'] + 1
                                        nick1 = ochko21_q[groupchat][wet]['nick1']
                                        msg(groupchat, nick1+u': ваш ход')
                                        return
                                if parameters == u'хватит':
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'за игру вы набрали '+asf+u' очков, Поздрасляю вас!')
                                        ochko21_q[groupchat][jid]['xod1'] = 5
                                        ochko21_q[groupchat][jid]['xod2'] = 3
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        ochko21_q[groupchat][wet]['xod1'] = 0
                                        ochko21_q[groupchat][wet]['xod2'] = 3
                                        nick1 = ochko21_q[groupchat][wet]['nick1']
                                        msg(groupchat, nick1+u': ваш ход')
                                        return

                if ochko21_q[groupchat][jid]['xod2'] == 1:
                        if ochko21_q[groupchat][jid]['xod']==1 or ochko21_q[groupchat][jid]['xod']==3 or ochko21_q[groupchat][jid]['xod']==5 or ochko21_q[groupchat][jid]['xod']==7 or ochko21_q[groupchat][jid]['xod']==9 or ochko21_q[groupchat][jid]['xod']==11 or ochko21_q[groupchat][jid]['xod']==13: 
                                if parameters == u'карту':
                                        ochko21_q[groupchat][jid]['xod'] = ochko21_q[groupchat][jid]['xod'] + 1
                                        hh = random.choice(ochko21)
                                        ochko21_q[groupchat][jid]['ochko21'] = ochko21_q[groupchat][jid]['ochko21'] + 1
                                        if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                                hh = random.choice(ochko21)
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh == u'6_крести' or hh == u'6_пики':
                                                k = 6
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'6_черви' or hh == u'6_буби':
                                                k = 6
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'7_крести' or hh == u'7_пики' or hh == u'7_черви' or hh == u'7_буби':
                                                k = 7
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'8_крести' or hh == u'8_пики' or hh == u'8_черви' or hh == u'8_буби':
                                                k = 8
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'9_крести' or hh == u'9_пики' or hh == u'9_черви' or hh == u'9_буби':
                                                k = 9
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'10_крести' or hh == u'10_пики' or hh == u'10_черви' or hh == u'10_буби':
                                                k = 10
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'валет_крести' or hh == u'валет_пики' or hh == u'валет_черви' or hh == u'валет_буби':
                                                k = 2
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'дама_крести' or hh == u'дама_пики' or hh == u'дама_черви' or hh == u'дама_буби':
                                                k = 3
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'кароль_крести' or hh == u'кароль_пики' or hh == u'кароль_черви' or hh == u'кароль_буби':
                                                k = 4
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if hh == u'туз_крести' or hh == u'туз_пики' or hh == u'туз_черви' or hh == u'туз_буби':
                                                k = 11
                                                ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                        if ochko21_q[groupchat][jid]['ochko21']==2:
                                                ochko21_q[groupchat][jid]['karta1'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==4:
                                                ochko21_q[groupchat][jid]['karta2'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==6:
                                                ochko21_q[groupchat][jid]['karta3'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==8:
                                                ochko21_q[groupchat][jid]['karta4'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==10:
                                                ochko21_q[groupchat][jid]['karta5'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==12:
                                                ochko21_q[groupchat][jid]['karta6'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==14:
                                                ochko21_q[groupchat][jid]['karta7'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==16:
                                                ochko21_q[groupchat][jid]['karta8'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==18:
                                                ochko21_q[groupchat][jid]['karta9'] = hh
                                        if ochko21_q[groupchat][jid]['ochko21']==20:
                                                ochko21_q[groupchat][jid]['karta10'] = hh
                                        if ochko21_q[groupchat][jid]['ochki'] > 21:
                                                asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                                reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf+u' очков. Вы проиграли!')
                                                ochko21_q[groupchat][jid]['xod1'] = 5
                                                ochko21_q[groupchat][jid]['xod2'] = 3
                                                wet = ochko21_q[groupchat][jid]['jid3']
                                                ochko21_q[groupchat][wet]['xod1'] = 0
                                                ochko21_q[groupchat][wet]['xod2'] = 3
                                                nick1 = ochko21_q[groupchat][wet]['nick1']
                                                msg(groupchat, nick1+u': ваш ход')
                                                return
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf)
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        ochko21_q[groupchat][wet]['xod'] = ochko21_q[groupchat][wet]['xod'] + 1
                                        nick1 = ochko21_q[groupchat][wet]['nick1']
                                        msg(groupchat, nick1+u': ваш ход')
                                        return
                                if parameters == u'хватит':
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'за игру вы набрали '+asf+u' очков, Поздрасляю вас!')
                                        ochko21_q[groupchat][jid]['xod1'] = 5
                                        ochko21_q[groupchat][jid]['xod2'] = 3
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        ochko21_q[groupchat][wet]['xod1'] = 0
                                        ochko21_q[groupchat][wet]['xod2'] = 3
                                        nick1 = ochko21_q[groupchat][wet]['nick1']
                                        msg(groupchat, nick1+u': ваш ход')
                                        return

                if ochko21_q[groupchat][jid]['xod1'] == 0:
                        if parameters == u'карту':
                                ochko21_q[groupchat][jid]['xod'] = ochko21_q[groupchat][jid]['xod'] + 1
                                hh = random.choice(ochko21)
                                ochko21_q[groupchat][jid]['ochko21'] = ochko21_q[groupchat][jid]['ochko21'] + 1
                                if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                        hh = random.choice(ochko21)
                                if hh in ochko21_q[groupchat][jid]['karta1'] or hh in ochko21_q[groupchat][jid]['karta2'] or hh in ochko21_q[groupchat][jid]['karta3'] or hh in ochko21_q[groupchat][jid]['karta4'] or hh in ochko21_q[groupchat][jid]['karta5'] or hh in ochko21_q[groupchat][jid]['karta6'] or hh in ochko21_q[groupchat][jid]['karta7'] or hh in ochko21_q[groupchat][jid]['karta8'] or hh in ochko21_q[groupchat][jid]['karta9'] or hh in ochko21_q[groupchat][jid]['karta10']:
                                        hh = random.choice(ochko21)
                                if ochko21_q[groupchat][jid]['jid3'] != u'0':
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                        if hh in ochko21_q[groupchat][wet]['karta1'] or hh in ochko21_q[groupchat][wet]['karta2'] or hh in ochko21_q[groupchat][wet]['karta3'] or hh in ochko21_q[groupchat][wet]['karta4'] or hh in ochko21_q[groupchat][wet]['karta5'] or hh in ochko21_q[groupchat][wet]['karta6'] or hh in ochko21_q[groupchat][wet]['karta7'] or hh in ochko21_q[groupchat][wet]['karta8'] or hh in ochko21_q[groupchat][wet]['karta9'] or hh in ochko21_q[groupchat][wet]['karta10']:
                                                hh = random.choice(ochko21)
                                if hh == u'6_крести' or hh == u'6_пики':
                                        k = 6
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'6_черви' or hh == u'6_буби':
                                        k = 6
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'7_крести' or hh == u'7_пики' or hh == u'7_черви' or hh == u'7_буби':
                                        k = 7
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'8_крести' or hh == u'8_пики' or hh == u'8_черви' or hh == u'8_буби':
                                        k = 8
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'9_крести' or hh == u'9_пики' or hh == u'9_черви' or hh == u'9_буби':
                                        k = 9
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'10_крести' or hh == u'10_пики' or hh == u'10_черви' or hh == u'10_буби':
                                        k = 10
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'валет_крести' or hh == u'валет_пики' or hh == u'валет_черви' or hh == u'валет_буби':
                                        k = 2
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'дама_крести' or hh == u'дама_пики' or hh == u'дама_черви' or hh == u'дама_буби':
                                        k = 3
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'кароль_крести' or hh == u'кароль_пики' or hh == u'кароль_черви' or hh == u'кароль_буби':
                                        k = 4
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if hh == u'туз_крести' or hh == u'туз_пики' or hh == u'туз_черви' or hh == u'туз_буби':
                                        k = 11
                                        ochko21_q[groupchat][jid]['ochki'] = ochko21_q[groupchat][jid]['ochki'] + k
                                if ochko21_q[groupchat][jid]['ochko21']==1:
                                        ochko21_q[groupchat][jid]['karta1'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==2:
                                        ochko21_q[groupchat][jid]['karta2'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==3:
                                        ochko21_q[groupchat][jid]['karta3'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==4:
                                        ochko21_q[groupchat][jid]['karta4'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==5:
                                        ochko21_q[groupchat][jid]['karta5'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==6:
                                        ochko21_q[groupchat][jid]['karta6'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==7:
                                        ochko21_q[groupchat][jid]['karta7'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==8:
                                        ochko21_q[groupchat][jid]['karta8'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==9:
                                        ochko21_q[groupchat][jid]['karta9'] = hh
                                if ochko21_q[groupchat][jid]['ochko21']==10:
                                        ochko21_q[groupchat][jid]['karta10'] = hh
                                if ochko21_q[groupchat][jid]['ochki'] > 21:
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf+u' очков. Вы проиграли!')
                                        del ochko21_q[groupchat]
                                        return
                                asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                reply(type,source,u'вам выпала карта '+hh+u', общее количество очков у вас '+asf+u'. Введите команду "карту", если вам нужно ещё, или введите команду "хватит"')
                        if parameters == u'хватит':
                                if ochko21_q[groupchat][jid]['jid3'] != u'0':
                                        wet = ochko21_q[groupchat][jid]['jid3']
                                        nick1 = ochko21_q[groupchat][wet]['nick1']
                                        if ochko21_q[groupchat][wet]['ochki'] > 21:
                                                asf = unicode(ochko21_q[groupchat][jid]['ochki']) 
                                                reply(type,source,u'за игру вы набрали '+asf+u' очков. Поздрасляю вас, вы выиграли!')
                                                msg(groupchat, nick1+u': за игру вы набрали '+unicode(ochko21_q[groupchat][wet]['ochki'])+u' очков. Вы проиграли!')
                                                del ochko21_q[groupchat]
                                                return
                                        else:
                                                if ochko21_q[groupchat][jid]['ochki'] == ochko21_q[groupchat][wet]['ochki']:
                                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                                        ert = ochko21_q[groupchat][wet]['ochki']
                                                        reply(type,source,u'за игру вы набрали '+asf+u' очков. Поздрасляю вас, у вас ничья!')
                                                        msg(groupchat, nick1+u': за игру вы набрали '+unicode(ert)+u' очков. Поздрасляю вас, у вас ничья!')
                                                        del ochko21_q[groupchat]
                                                        return
                                                else:
                                                        if ochko21_q[groupchat][jid]['ochki'] > ochko21_q[groupchat][wet]['ochki']:
                                                                asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                                                ert = ochko21_q[groupchat][wet]['ochki']
                                                                reply(type,source,u'за игру вы набрали '+asf+u' очков. Поздрасляю вас, вы выиграли!')
                                                                msg(groupchat, nick1+u': за игру вы набрали '+unicode(ert)+u' очков. Вы проиграли!')
                                                                del ochko21_q[groupchat]
                                                                return
                                                        else:
                                                                asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                                                ert = ochko21_q[groupchat][wet]['ochki']
                                                                reply(type,source,u'за игру вы набрали '+asf+u' очков. Вы проиграли!')
                                                                msg(groupchat, nick1+u': за игру вы набрали '+unicode(ert)+u' очков. Поздрасляю вас, вы выиграли!')
                                                                del ochko21_q[groupchat]
                                                                return
                                else:
                                        asf = unicode(ochko21_q[groupchat][jid]['ochki'])
                                        reply(type,source,u'за игру вы набрали '+asf+u' очков, Поздрасляю вас!')
                                        del ochko21_q[groupchat]
                                        return

register_message_handler(ochko21_msg)
register_command_handler(ochko21_start, 'очко', ['мук','все'], 10, 'Стартует игру с ботом или вдвоем в 21 очко', 'очко', ['очко'])
