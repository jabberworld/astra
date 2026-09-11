#===istalismanplugin===
# -*- coding: utf-8 -*-



def handler_1(type, source, nick):
   if type == 'private':
      reply(type, source, u'Работает только в чате!')
      return
   if not nick:
      reply(type,source,u'Каго запускать будим?')
      return
   if nick == handler_botnick(source[1]):
      reply(type, source, u'Щас тебя запущу ]:->')
      return
   if nick in GROUPCHATS[source[1]]:
      msg(source[1], u'/me Запускаю спутник '+nick)
      time.sleep(1)
      msg(source[1],u'адын')
      time.sleep(1)
      msg(source[1],u'двыа')
      time.sleep(1)
      msg(source[1],u'тры')
      time.sleep(1)
      msg(source[1],u'чятыре')
      time.sleep(1)
      msg(source[1],u'пииаать')
      time.sleep(1)
      msg(source[1],u'ыыыыыыть')
      time.sleep(1)
      handler_kick(source[1], nick, u'Приятного  полета')
      time.sleep(1)
      msg(source[1], nick+u', Приятного полета')
      return
   else:
      reply(type, source, u'кого!? нет таких тут!')
      return

register_command_handler(handler_1, 'спутник', [], 10, 'Запускает юзверя в космос', 'спутник ник', ['спутник ник'])

