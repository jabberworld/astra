#===istalismanplugin===
# -*- coding: utf-8 -*-

def spam(type,source,body):
   if type == 'private':
      reply(type,source,u'Только чат.....')
      return
   if not body:
      reply(type,source,u'Каго глумить буим? ;-)')
      return
   if body.count('@'):
      msg(source[1],u'Маладец боец.... Я уже настучала админам жабы.....теряйся вонючий спамер....они уже идут за тобой')
      return

register_command_handler(spam, 'спамжид', [], 10, 'Спамит жид юзера в течении 15-ти минут.', 'спамжид жид', ['спамжид user@jabber.ru'])