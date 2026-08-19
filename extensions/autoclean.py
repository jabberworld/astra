#===istalismanplugin===
# -*- coding: utf-8 -*-

AUTOCLEAN = {}

def auto_clean_work(raw,mType,source,body):
   if mType != 'private':
      if source[1] in AUTOCLEAN.keys():
         if len(body) >= 512:
            handler_clean(mType, source, 'тихо')            
      else:
         return
   else:
      return

register_message_handler(auto_clean_work)

def auto_clean_control(type,source,body):
   if body in [u'вкл',u'1',u'on']:
      if source[1] not in AUTOCLEAN.keys():
         AUTOCLEAN[source[1]] = 1
         reply(type,source,u'Включено')
      else:
         reply(type,source,u'Уже включено')
   if body in [u'выкл',u'0',u'off']:
      if source[1] in AUTOCLEAN.keys():
         del AUTOCLEAN[source[1]]
         reply(type,source,u'Выключено')
      else:
         reply(type,source,u'и так выключено')
   if not body:
      if source[1] not in AUTOCLEAN.keys():
         reply(type,source,u'выключено')
      else:
         reply(type,source,u'включено')

register_command_handler(auto_clean_control, 'авточисть', [], 20, 'чистка чата если сообщение от пользователя превышает 512 символов', 'авточисть вкл', ['авточисть'])