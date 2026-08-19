#===istalismanplugin===
# /* coding: utf-8 */

SEND_CACHE1 = {}

def handler_send_save1(raw, type, source, body):
   if source[1] in GROUPCHATS:
      args = body.split()
      if len(args) >= 2:
         date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
         fromnick = u'%s попросил (%s) меня передать тебе следующее:\n\n' % (source[2], date)
         nick = args[0].strip()
         body = body[(body.find(' ') + 1):].strip()
         if len(body) <= 1024:
            if nick.count(u'Олег'):
               jid = handler_jid(source[0])
               if jid in AMSGBL:
                  reply(ltype, source, u'тебе запрещено отсылать мессаги админу')
               else:
                  delivery(u'*<>*<>*<>*<>*<>*<>*<>*\nСообщение от '+source[2]+' ('+jid+'): Олег '+body+u'\n*<>*<>*<>*<>*<>*<>*')
                  reply(type, source, u'Передала :)')
                  return
            #sym1 = [',','>',':']
            elif nick.count(':') > 0 or nick.count(',') > 0:
               for sym in (',',':','>'):
                  nick = nick.replace(sym, '')
               if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
                  return
               else:
                  if nick in GROUPCHATS[source[1]]:
                     if not nick in SEND_CACHE1[source[1]]:
                        SEND_CACHE1[source[1]][nick] = []
                     SEND_CACHE1[source[1]][nick].append(fromnick+body)
                     write_file('dynamic/'+source[1]+'/send1.txt', str(SEND_CACHE1[source[1]]))
                     reply(type, source, u'Как зайдёт обязательно передам :)')

def handler_send_join1(conf, nick, afl, role):
        if nick in SEND_CACHE1[conf]:
                for body in SEND_CACHE1[conf][nick]:
                        msg(conf+'/'+nick, u'*<>*<>*<>*<>*<>*<>*\n'+body+u'\n*<>*<>*<>*<>*<>*<>*')
                del SEND_CACHE1[conf][nick]
                write_file('dynamic/'+conf+'/send1.txt', str(SEND_CACHE1[conf]))

def get_send_cache1(conf):
        if check_file(conf, 'send1.txt'):
                cache1 = load_file('dynamic/'+conf+'/send1.txt', {})
        else:
                cache1 = {}
                delivery(u'Внимание! Не удалось создать send1.txt для "%s"!' % (conf))
        SEND_CACHE1[conf] = cache1

register_join_handler(handler_send_join1)
register_message_handler(handler_send_save1)

register_stage1_init(get_send_cache1)
