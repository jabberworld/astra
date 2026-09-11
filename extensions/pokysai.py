#===istalismanplugin===
# -*- coding: utf-8 -*-

def hnd_pokysai(type,source,body):
   if body == handler_botnick(source[1]):
      reply(type,source,u'Щас тебя покусаю ]:->')
      return
   if not body:
      reply(type,source,u'Кому че откусить?')
      return
   if type=='private':
      reply(type,source,u'только в чате.')
   group=source[1]
   mis=[u'жопу',u'руку',u'ногу',u'нос',u'ухо']
   mes=random.choice(mis)
   if source[1] not in POL_SEX.keys():
      msg(group,u'/me покусала '+body+' за '+mes)
   else:
      msg(group,u'/me покусал '+body+' за '+mes)

register_command_handler(hnd_pokysai, 'покусай', [], 10, 'кусает юзера', 'покусай ник', ['покусай Кот'])

def hnd_atata(type,source,body):
   if body == handler_botnick(source[1]):
      reply(type,source,u'Щас тебя драть буду ]:->')
      return
   if not body:
      reply(type,source,u'Кого драть будим?')
      return
   if type=='private':
      reply(type,source,u':-D')
   group=source[1]
   dar=body
   if source[1] not in POL_SEX.keys():
      msg(group,random.choice([u'дала %s по жопе',u'надрала попу %s',u'провела %s попой по наждачке...',u'намазала попку %s скипидаром......',u'посадила %s попой на горячую сковородку',u'засунула в попу %s дробовик и перезарядила его',u'посадила %s попой на ножку стула и заставила двигаться вверх вниз']) % dar)
   else:
      msg(group,random.choice([u'дал %s по жопе',u'надрал попу %s',u'провел %s попой по наждачке...',u'намазал попку %s скипидаром......',u'посадил %s попой на горячую сковородку',u'засунул в попу %s дробовик и перезарядил его',u'посадил %s попой на ножку стула и заставил двигаться вверх вниз']) % dar)

register_command_handler(hnd_atata, 'атата', [], 10,  'дает по жопе юзеру', 'атата ник', ['атата Кот'])


