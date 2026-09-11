#===istalismanplugin===
# -*- coding: utf-8 -*-

POL_SEX = {}

def mode_control(type, source, body):
   if body == '1':
      if source[1] in POL_SEX.keys():
         reply(type,source,u'И так включено.')
         return
      POL_SEX[source[1]] = body
      reply(type, source, 'Сделала операцию по смену пола :-D')
      handler_set_botnick(type, source, u'.:AngeL:.')
   elif body == '0':
      if source[1] in POL_SEX.keys():
         del POL_SEX[source[1]]
         reply(type, source, u'Перешла в нормальный режим.')
         handler_set_botnick(type,source,u'Astra')
      else:
         reply(type,source,u'И так в нормальном режиме.')
   else:
      if source[1] in POL_SEX.keys():
         reply(type,source,u'Включено')
      else:
         reply(type,source,u'Выключено')

register_command_handler(mode_control, 'режим', [], 30, 'Меняет режим бота', 'режим 1', ['режим 0'])
