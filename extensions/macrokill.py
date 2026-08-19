# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  macrokill_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_set_botnick(type, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        nick = replace_all(body, {' ': '_', '"': '', "'": ''})
                        if len(nick) <= 16:
                                BOT_NICKS[source[1]] = nick
                                save_conflist(source[1], nick)
                                send_join_presece(source[1], nick)
                                reply(type, source, u'Зашифровалась под ником "%s"\n Перезахожу в чат для установки новых параметров.' % (nick))
                                body = source[1]
                                handler_admin_rejoin(type, source, body)
                        else:
                                reply(type, source, u'Нее! в моём нике не более 16 символов')
                else:
                        reply(type, source, u'инвалид синтакс')
        else:
                reply(type, source, u'чё упал чтоли!?')

def handler_conflist(type, source, body):
        repl = u'\n№ [Конфа] [Ник] [Pf] [Юзеров] [статус]'
        col = 0
        for conf in sorted(GROUPCHATS.keys()):
                col = col + 1
                online = 0
                botnick = handler_botnick(conf)
                for user in GROUPCHATS[conf]:
                        if GROUPCHATS[conf][user]['ishere']:
                                online = online + 1
                if conf in PREFIX:
                        pfx = PREFIX[conf]
                else:
                        pfx = u'нет'
                if conf in UNAVALABLE:
                        ismoder = u'Внимание!! Нет прав!!'
                else:
                        ismoder = u'модер'
                repl += '\n%s. %s [%s] "%s" (%s) - %s' % (str(col), conf, botnick, pfx, str(online), ismoder)
        if col != 0:
                if type == 'public':
                        reply(type, source, u'глянь в приват')
                reply('private', source, repl)
        else:
                reply(type, source, u'А меня нет ни в одной конверенции!')

def command_chatlist(type, source, body):
        if not body:
                cList = u"\nСписок конференций, в которых"\
                        u" сидит бот (всего %d штук):\n" % len(GROUPCHATS.keys())
                for x, y in enumerate(sorted(GROUPCHATS.keys())):
                        cList += u"• %d. %s\n" % (x + 1, y)
                if type == "public":
                        reply(type, source, u"Смотри в привате.") 
                reply("private", source, cList)
        elif body.strip() == "количество":
                reply(type, source, u"Количество обслуживаемых конференций: %d." % len(GROUPCHATS.keys()))
        

def handler_visitors(type, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        action = body.lower()
                else:
                        action = 'default'
                if action in [u'сегодня', 'today']:
                        today = that_day()
                        userlist = ''
                        usrcol = 0
                        col = 0
                        for user in sorted(GROUPCHATS[source[1]].keys()):
                                if not GROUPCHATS[source[1]][user]['ishere']:
                                        join_date = GROUPCHATS[source[1]][user]['join_date']
                                        if today == join_date[0]:
                                                usrcol = usrcol + 1
                                                userlist += '\n%s. %s (%s)' % (str(usrcol), user, handler_jid(source[1]+'/'+user))
                                else:
                                        col = col + 1
                        if usrcol != 0:
                                if type == 'public':
                                        reply(type, source, u'глянь в приват')
                                reply('private', source, (u'Сегодня здесь было %s юзеров:' % str(usrcol))+userlist+(u'\n+ ещё %s досихпор здесь' % str(col)))
                        else:
                                reply(type, source, u'Сегодня при мне ещё никто не выходил, все кто был досихпор здесь!')
                elif action in [u'даты', 'dates']:
                        userlist = ''
                        usrcol = 0
                        for user in sorted(GROUPCHATS[source[1]].keys()):
                                usrcol = usrcol + 1
                                join_date = GROUPCHATS[source[1]][user]['join_date']
                                userlist += '\n%s. %s %s' % (str(usrcol), user, time.strftime('%d.%m.%Y (%H:%M:%S)', join_date[1]))
                        if type == 'public':
                                reply(type, source, u'глянь в приват')
                        reply('private', source, (u'При мне заходило %s юзеров:' % str(usrcol))+userlist)
                elif action in [u'лист', 'list']:
                        users = []
                        for user in GROUPCHATS[source[1]]:
                                users.append(user)
                        usrcol = len(users)
                        if type == 'public':
                                reply(type, source, u'глянь в приват')
                        reply('private', source, (u'При мне заходило %s юзеров: ' % str(usrcol))+', '.join(sorted(users)))
                else:
                        userlist = ''
                        usrcol = 0
                        col = 0
                        for user in sorted(GROUPCHATS[source[1]].keys()):
                                if not GROUPCHATS[source[1]][user]['ishere']:
                                        usrcol = usrcol + 1
                                        userlist += '\n%s. %s (%s)' % (str(usrcol), user, handler_jid(source[1]+'/'+user))
                                else:
                                        col = col + 1
                        if usrcol != 0:
                                if type == 'public':
                                        reply(type, source, u'глянь в приват')
                                reply('private', source, (u'Здесь было %s юзеров:' % str(usrcol))+userlist+(u'\n+ ещё %s до сих пор здесь' % str(col)))
                        else:
                                reply(type, source, u'При мне никто ещё не выходил, все, кто был, - до сих пор здесь!')
        else:
                reply(type, source, u'Я хз кто был у тебя в ростере :D')

A_TOPIC = {}
A_C = {}

def atopik_control(t,s,b):
    global A_C
    if b == u'1':
        reply(t,s,u'Включено')
        confa = s[1]
        A_C[confa] = b
        if confa in A_C.keys():
            while A_C[confa] != 0:
                time.sleep(3600)
                qipfr = read_file('static/status.txt').split('\n')
                JCON.send(xmpp.Message(str(s[1]), "", "groupchat", str.join('',A_TOPIC[confa])+'\n'+random.choice(qipfr)))
    elif b == u'0':
        confa = s[1]
        A_C[confa] = 0
        reply(t,s,u'Выключено')
    elif b == u'показать':
        confa = s[1]
        if confa in A_TOPIC.keys():
            reply(t,s,u'Текущий топик:\n%s' % str.join('',A_TOPIC[confa]))
        else:
            reply(t,s,u'Не установлено')
            return
    elif not b:
        confa = s[1]
        if confa in A_C.keys():
            if A_C[confa] == 0:
                reply(t,s,u'Атопик выключен')
            else:
                reply(t,s,u'Атопик включен')
                return
        else:
            reply(t,s,u'Атопик выключен')
    else:
        reply(t,s,u'Смотри хелп')

register_command_handler(atopik_control, 'атопик', [], 20, 'Включает, выключает или показывает атопик. Доступные параметры:\n1 - включить\n0 - выключить\nпоказать - показывает текущий топик.', 'атопик 1', ['атопик показать'])

def atopic_save(t, s, p):
        if not p:
            global A_TOPIC
            confa = s[1]
            if confa in A_TOPIC.keys():
                del A_TOPIC[confa]
                reply(t, s, u'Тема удалена')
                topic_save_now()
                return
            else:
                reply(t, s, u'И так не установлено!')
                return
        confa = s[1]
        if not confa in A_TOPIC.keys():
            A_TOPIC[confa] = p
            reply(t, s, u'Добавлено')
            topic_save_now()
        else:
            A_TOPIC[confa] = p
            reply(t, s, u'Обновлено!')
            topic_save_now()
        
def topic_load_now(*list):
        global A_TOPIC
        try:
                fp = file('dynamic/atopic.txt', 'r')
                A_TOPIC = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/atopic.txt', 'w')
                A_TOPIC = {}
                fp.write( str(A_TOPIC) )
                fp.close()

def topic_save_now():
        global A_TOPIC
        fp = file('dynamic/atopic.txt', 'w')
        fp.write( str(A_TOPIC) )
        fp.close()

register_stage1_init(topic_load_now)
register_command_handler(atopic_save, 'атопик*', [], 20, 'Добавляет в тему чата афоризм каждые десять минут, если текст оставить пустым удаляет.', 'атопик текст', ['атопик текст'])

def handler_topic(type, source, body):
        if body:
                body = replace_all(body, {'<': u'«', '>': u'»'})
                try:
                        JCON.send(xmpp.Message(unicode(source[1]), "", "groupchat", body))
                except:
                        reply(type, source, u'Не отправляется как-то эта хрень...')
        else:
                reply(type, source, u'И где тут топег?')

command_handler(handler_set_botnick, 30, "macrokill")
command_handler(handler_visitors, 20, "macrokill")
command_handler(handler_conflist, 80, "macrokill")
command_handler(command_chatlist, 20, "macrokill")
command_handler(handler_topic, 20, "macrokill")
