#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

def hnd_kypit(t,s,p):
   jid = handler_jid(s[0])
   
   if UZVER[jid]['lokacia'] == 2:
      if p in [u'рыбу']:
         if not u'riba' in UZVER[jid]:
            UZVER[jid]['riba'] = 0
         UZVER[jid]['riba'] += 1
         reply(t,s,u'*OK*')

register_command_handler(hnd_kypit, 'купить', [], 0, '', '', [''])