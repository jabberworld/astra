#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

metla = {}

def metla1(t,s,p):
   jid = handler_jid(s[0])
   if not jid in metla:
      metla[jid] = 0
   if p == s[2]:
      reply(t,s,u'Че сам себя погонять решил? :-D')
      return
   if p == handler_botnick(s[1]):
      reply(t,s,u'щас тебя гонять буду! ]:->')
      return
   if p in GROUPCHATS[s[1]]:
      msg(s[1],u'/me гоняет метлой '+p+u' по всему чату')
      return
   else:
      if metla[jid] >= 1:
         metla[jid] = 0
         msg(s[1],u'/me припарковала мeтлу '+s[2]+u' в угол')
         return
      else:
         reply(t,s,u'а я тебе мeтлу и не давала :-P')
         return

register_command_handler(metla1, 'метла', [], 11, '', '', [''])

def metlu(t,s,p):
   jid = handler_jid(s[0])
   if p in GROUPCHATS[s[1]]:
      jid1 = handler_jid(s[1]+'/'+p)
      if not jid1 in metla:
         metla[jid1] = 0
      if metla[jid1] <= 0:
         metla[jid1] = 1
         msg(s[1], u'/me притаранила мeтлу '+p)
         return
      else:
         reply(t,s,u'Метлa и так у '+p)
         return
   else:
      if not jid in metla:
         metla[jid] = 0
      if metla[jid] >= 1:
         reply(t,s,u'метла и так у тебя :-|')
         return
      else:
         metla[jid] = 1
         msg(s[1],u'притаранила метлу '+s[2])
         return

register_command_handler(metlu, 'метлу', [], 0, '', '', [''])