#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

VER_FILENAME = 'static/versions.txt'

Caps = 'http://miranda-im.org/caps'
CapsVer = '%s.%s' % (BOT_VER, CORE_MODE)

def botversion(t,s,p):
   VERSION_BOT = load_file(VER_FILENAME, {})
   if not p:
      reply(t,s,u'Ботверсия: \nИмя: '+str(NONAME)+u'\nВерсия: '+str(BOT_VER)+u' (r.'+str(BOT_REV)+u')\nКлиент: '+str(os_name))
      return
   if p.count(u'&') < 4:
                   reply(t, s, u'чё за бред?!1 кури помощь по команде')
                   return
   args = p.split(u'&')
   VERSION_BOT[NONAME] = args[0].strip()
   VERSION_BOT[BOT_VER] = args[1].strip()
   VERSION_BOT[BOT_REV] = args[2].strip()
   VERSION_BOT[CORE_MODE] = args[3].strip()
   VERSION_BOT[os_name] = args[4].strip()
   write_file(VER_FILENAME, str(VERSION_BOT))
   reply(t,s,u'Ага, поняла, ща все поставлю')

def botver_state2_init():
   global VERSION_BOT
   for conf in GROUPCHATS.keys():
                   if initialize_file(VER_FILENAME, '{}'):
                      VERSION_BOT = load_file(VER_FILENAME, {})

register_stage2_init(botver_state2_init)
register_command_handler(botversion, 'шифруйся', [], 100, 'Меняет имя версии бота.', '', [''])