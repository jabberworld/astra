#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

RAMKA = {}

def ramka_control(type,source,body):
   if body in [u'вкл',u'1',u'on']:
      if source[1] not in RAMKA.keys():
         RAMKA[source[1]] = 1
         ramka_save_now()
         reply(type,source,u'Включено')
      else:
         reply(type,source,u'Уже включено')
   if body in [u'выкл',u'0',u'off']:
      if source[1] in RAMKA.keys():
         del RAMKA[source[1]]
         ramka_save_now()
         reply(type,source,u'Выключено')
      else:
         reply(type,source,u'и так выключено')
   if not body:
      if source[1] not in RAMKA.keys():
         reply(type,source,u'выключено')
      else:
         reply(type,source,u'включено')

def ramka_save_now():
        global RAMKA
        fp = file('dynamic/ramka.txt', 'w')
        fp.write( str(RAMKA) )
        fp.close()

def ramka_load_now(*list):
        global RAMKA
        try:
                fp = file('dynamic/ramka.txt', 'r')
                RAMKA = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/ramka.txt', 'w')
                RAMKA = {}
                fp.write( str(RAMKA) )
                fp.close()

register_stage1_init(ramka_load_now)
register_command_handler(ramka_control, 'рамка', [], 30, 'хрень', 'рамка вкл', ['рамка'])