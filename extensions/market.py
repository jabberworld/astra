#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

#MONEY = {}
VECHI = {}
USER_VECHI = {}

def hnd_market(t,s,p):
   jid = handler_jid(s[0])
   conf = s[1]
   nick = s[2]
   #if p in ['+', 'add', u'добавить']:
   if p:
      p = p.split(':', 2)
      #p = p.lower()
      if len(p) < 3:
         reply(t,s,u'Пиши так "предмет:цена:описание"')
         return
      if not p[0] in COMMANDS:
         if len(p[0]) <= 20:
            VECHI = p[0]
            if not p[1].isdigit():
               reply(t,s,u'Второй параметр должен быть числом')
               return
            #number = str(p[1])
            if p[2] == '':
               reply(t,s,u'Добавь описание-действие!')
               return
            VECHI[p[0]]['price'] = int(p[1])
            VECHI[p[0]]['opis'] = p[2]
            reply(t, s, u'Добавлено')
            return
         else:
            reply(t,s,u'Не длиннее 20 символов')
            return
      else:
         reply(t,s,u'Нельзя, это команда')
         return
   else:
      reply(t,s,u'ошибка')


register_command_handler(hnd_market, 'маркет+', [], 11, '', '', [''])