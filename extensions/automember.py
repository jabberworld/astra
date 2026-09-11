# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  automember.py

# Copyright © Assassin, 2012
# This program published under Apache 2.0 license
# See LICENSE.txt for more details
# My EMail: assassin@sonikelf.ru
# My XMPP-conference: bottiks@conference.jabber.ru
# My Site: bottiks.ucoz.ru
CONFRULES = {}
CONFRULES = dict()
confrules_member = lambda conf, nick: (handler_member(conf, nick, u'Время автомембера прошло') if GROUPCHATS[conf][nick]['ishere'] else None)# если юзер ещё в конфе то делает его мембером

def confrules_join(conf, nick, afl, role):
        if conf in CONFRULES and afl == 'none':# если в конфе включён автомемебер и юзер заходит без мембера
                if role != 'visitor': handler_visitor(conf, nick, u'Автомембер')# если он еще не визитор то делаем его таковым
                threading.Timer(CONFRULES[conf][0], confrules_member, (conf, nick,)).start()# запускаем таймер в фоне на делание мемебром
                if CONFRULES[conf][1]: msg(conf + '/' + nick, str.join(' ', CONFRULES[conf][1]))# если настроены правила то отправляем их в приват

def confrules_control(type, source, body):
        conf = source[1]
        body = body.split()
        if conf in GROUPCHATS.keys():
                rep = u'Сделано'
                if not body:
                        if conf in CONFRULES:
                                rep = u'Время: ' + str(CONFRULES[conf][0]) + chr(10)
                                if CONFRULES[conf][1]: rep += u'Правила: '+ str.join(' ',CONFRULES[conf][1])
                                else: rep += u'Правил нет'
                        else: rep = u'В этой конференции автомембер не активирован'
                elif (body[0] in [u'нет', u'выкл', '0']):
                        if conf in CONFRULES:
                                del CONFRULES[conf]
                                write_file('dynamic/%s/confrules.txt' % (conf), 'off')
                        else: rep = u'И так выключено'
                elif check_number(body[0]):
                        CONFRULES[conf] = (int(body[0]), (body[1:] if len(body) > 2 else False),)
                        write_file('dynamic/%s/confrules.txt' % (conf), str(CONFRULES[conf]))
                else: rep = u'Неверные параметры'
        else: rep = u'Команда действительна только в конференции!'
        reply(type, source, rep)

def confrules_init(conf):
        if check_file(conf, 'confrules.txt', "off"):
                temp = read_file('dynamic/%s/confrules.txt' % (conf))
                if temp != 'off': CONFRULES[conf] = eval(temp)
        else: delivery(u'Внимание! Не удалось создать confrules.txt для "%s"!' % (conf))

register_join_handler(confrules_join)
register_command_handler(confrules_control, 'автомембер', [], 20, 'дает юзеру мембера через определенное время', 'автомембер 120', ['автомембер 120'])
register_stage1_init(confrules_init)