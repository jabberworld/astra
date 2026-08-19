#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

def hnd_lokacia(t,s,p):
   jid = handler_jid(s[0])
   if t != 'private':
      reply(t,s,u'пиши в приват!')
      return
   if not jid in UZVER:
      UZVER[jid] = {'lokacia': 0}
      with file('dynamic/uzver.txt', 'w') as fp: fp.write(str(UZVER))
   if p in [u'дом']:
      if UZVER[jid]['lokacia'] == 2:
         reply(t,s,u'хе хе телепорты еще не придуманы :D выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 0:
         reply(t,s,u'ты и так дома!')
         return
      if UZVER[jid]['lokacia'] == 3:
         reply(t,s,u'Ты в лесу, сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 4:
         reply(t,s,u'Ты в Казино, сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 1:
         UZVER[jid]['lokacia'] = 0
         msg(s[1],u'/me '+s[2]+u' заходит домой.')
         reply(t,s,u'*OK*')
         return
   if p in [u'улица']:
      if UZVER[jid]['lokacia'] == 1:
         reply(t,s,u'ты и так на улице!')
         return
      else:
         UZVER[jid]['lokacia'] = 1
         msg(s[1],u'/me '+s[2]+u' вышел на Широкую улицу расположенную в центре города.')
         reply(t,s,u'*OK*')
         return
   if p in [u'магазин']:
      if UZVER[jid]['lokacia'] == 0:
         reply(t,s,u'хе хе телепорты еще не придуманы :D сначала выйди на улицу!')
         return
      if UZVER[jid]['lokacia'] == 3:
         reply(t,s,u'Ты в лесу, иди на улицу')
         return
      if UZVER[jid]['lokacia'] == 2:
         reply(t,s,u'ты и так в магазине!')
         return
      if UZVER[jid]['lokacia'] == 4:
         reply(t,s,u'Ты в Казино, иди на улицу')
         return
      if UZVER[jid]['lokacia'] == 1:
         UZVER[jid]['lokacia'] = 2
         msg(s[1],u'/me '+s[2]+u' зашел в магазин "Всакая всячина"')
         reply(t,s,u'Витрина: \n• хлеб\n• пиво\n• нож\n• куртка\n• аспирин\n• металлоискатель\n• бейсбольная бита\n• джинсы\n• шапка\n• \n• монеты \n• удочка')
         return
   if p in [u'озеро']:
      if UZVER[jid]['lokacia'] == 2:
         reply(t,s,u'хе хе телепорты еще не придуманы :D выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 0:
         reply(t,s,u'Ты дома, выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 3:
         reply(t,s,u'Ты в лесу, сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 4:
         reply(t,s,u'Ты в Казино, сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 5:
         reply(t,s,u'Ты и так на озере')
         return
      if UZVER[jid]['lokacia'] == 1:
         UZVER[jid]['lokacia'] = 5
         msg(s[1],u'/me '+s[2]+u' вышел на Песчанный берег Прозрачного Озера, неподалеку от леса.')
         reply(t,s,u'*OK*')
         return
   if p in [u'лес']:
      if UZVER[jid]['lokacia'] == 3:
         reply(t,s,u'Ты и так в лесу')
         return
      if UZVER[jid]['lokacia'] == 0:
         reply(t,s,u'хе хе телепорты еще не придуманы :D сначала выйди на улицу!')
         return
      if UZVER[jid]['lokacia'] == 2:
         reply(t,s,u'ты в магазине! Сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 1:
         UZVER[jid]['lokacia'] = 3
         msg(s[1],u'/me '+s[2]+u' лазит по глухой чаще старинного леса....')
         reply(t,s,u'*OK*')
         return
   if p in ['казино']:
      if UZVER[jid]['lokacia'] == 3:
         reply(t,s,u'Ты в лесу, иди сначала на улицу')
         return
      if UZVER[jid]['lokacia'] == 0:
         reply(t,s,u'хе хе телепорты еще не придуманы :D сначала выйди на улицу!')
         return
      if UZVER[jid]['lokacia'] == 2:
         reply(t,s,u'ты в магазине! Сначала выйди на улицу')
         return
      if UZVER[jid]['lokacia'] == 4:
         reply(t,s,u'Ты и так в казино!')
         return
      if UZVER[jid]['lokacia'] == 1:
         UZVER[jid]['lokacia'] = 4
         msg(s[1],u'/me '+s[2]+u' зашел в Казино')
         reply(t,s,u'*OK*')
         return
   else:
      if UZVER[jid]['lokacia'] == 0:
         repl = u'Дом'
      if UZVER[jid]['lokacia'] == 1:
         repl = u'Улица'
      if UZVER[jid]['lokacia'] == 2:
         repl = u'Магазин'
      if UZVER[jid]['lokacia'] == 3:
         repl = u'Лес'
      if UZVER[jid]['lokacia'] == 4:
         repl = u'Казино'
      if UZVER[jid]['lokacia'] == 5:
         repl = u'Озеро'
      reply(t,s,u'Местонахождение:\n Локация: '+repl+u'\nДоступные локации: Дом, Улица, Магазин, Казино, Лес, Озеро')

register_command_handler(hnd_lokacia, '#', [], 0, '', '', [''])