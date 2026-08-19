#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

strelka = {}

def strelka_control(t,s,p):
   jid = handler_jid(s[0])
   user_jid = handler_jid(s[1]+'/'+p)
   if not p:
      reply(t,s,u'за кем следить собралсо?')
      return
   if p == handler_botnick(s[1]):
      reply(t,s,u'Как ты себе это представляешь?!!')
      return
   if p in GROUPCHATS[s[1]]:
      if user_jid in strelka:
         reply(t,s,u'И так слежу за ним...')
         return
      strelka[user_jid] = jid
      reply(t,s,u'как увижу сообщу')
   else:
      reply(t,s,u'такого не знаю')

def strelka_del(t,s,p):
   user_jid = handler_jid(s[1]+'/'+p)
   if not p:
      reply(t,s,u'я хз че ты хочешь')
      return
   if user_jid in strelka:
      del strelka[user_jid]
      reply(t,s,u'больше не слежу за '+p)
   else:
      reply(t,s,u'я за ним и не слежу')

register_command_handler(strelka_del, 'неследи', [], 10, '', '', [''])

def join_strelka(conf, nick, afl, role):
   jid = handler_jid(conf+'/'+nick)
   if jid in strelka:
      msg(strelka[jid], u'юзер с ником '+nick+u' появился в чате '+conf)

register_join_handler(join_strelka)

register_command_handler(strelka_control, 'следи', [], 10, 'Позволяет вам следить за появлением юзера в чате.', 'следи ник', ['следи Кот'])
