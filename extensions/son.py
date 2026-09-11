#===istalismanplugin===
# -*- coding: utf-8 -*-

def hnd_son(type,source,body):
   if user_level(source[0], source[1]) >= 30:
      if body in [u'.',u'!',u'*']:
         handler_set_prefix(type,source,body)
         msg(source[1],u'Установлен префикс '+body)
      elif body in [u'какой?']:
         if source[1] in PREFIX:
            reply(type,source,u'Текущий префикс '+str(PREFIX[source[1]]))
         else:
            reply(type,source,u'Нет префикса')
      elif not body:
         handler_set_prefix(type,source,'*')
         msg(source[1],u'Установлен префикс *')
      else:
         reply(type,source,u'Издеваешься?!')
         return
   else:
      if source[1] in PREFIX:
         reply(type,source,u'Текущий префикс '+str(PREFIX[source[1]]))
      else:
         reply(type,source,u'Нет префикса')
         return

register_command_handler(hnd_son, 'префикс', [], 10, 'показывает текущий префикс или ставит префикс "*"', 'префикс', ['префикс'])

def hnd_astra(raw,type,source,body):
   if body==u'астра!':
      if user_level(source[0], source[1]) >= 30:
         if source[1] in PREFIX:
            del PREFIX[source[1]]
            write_file('dynamic/%s/prefix.txt' % (source[1]), "'none'")
            reply(type,source,u'Терь нет префикса!')
            message = STATUS[source[1]]['message']
            status = STATUS[source[1]]['status']
            change_bot_status(source[1], message, status)
         else:
            reply(type, source, u'Я туточки :)')
      else:
         reply(type,source, random.choice([u'М?', u'а?', u'Чаво?!!']))
   if body == u'астра':
      reply(type,source, random.choice([u'М?', u'а?', u'Чаво?!!']))

register_message_handler(hnd_astra)

TENE = {}

def son_energy(raw, type, source, body):
   confa = source[1]
   if body in [u'проснись',u'вставай',u'бельманда',u'инч сюды']:
      if confa in TENE.keys():
         if TENE[confa] < 150:
            if source[1] in PREFIX:
               reply(type, source, u'Отстааань...Спать хочу...')
            else:
               return
         else:
            if source[1] in PREFIX:
               del PREFIX[source[1]]
               write_file('dynamic/%s/prefix.txt' % (source[1]), "'none'")
               reply(type,source,u'Выспалась :)')
               message = STATUS[source[1]]['message']
               status = STATUS[source[1]]['status']
               change_bot_status(source[1], message, status)
            else:
               return
      return
   if body not in [u'проснись',u'вставай',u'бельманда',u'инч сюды']:
      return

register_message_handler(son_energy)
