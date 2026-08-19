# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  access_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_set_access(type, source, Params):
 if source[1] in GROUPCHATS:
  if Params:
   splitdata = Params.split()
   if len(splitdata) <= 3:
    item = splitdata[0].strip()
    if len(splitdata) >= 2:
     access = splitdata[1].strip()
    elif len(splitdata) == 1:
     access = '0'
    if check_number(access):
     if item.count('@') and item.count('.'):
      jidto = item
     elif item in GROUPCHATS[source[1]]:
      jidto = handler_jid(source[1]+'/'+item)
     else:
      jidto = False
     if jidto:
      jidsource = handler_jid(source[0])
      accjidsource = user_level(source[0], source[1])
      accjidto = user_level(jidto, source[1])
      if jidsource not in ADLIST:
       if jidto == jidsource or accjidto >= accjidsource or int(access) >= accjidsource:
        has_acc = False
       else:
        has_acc = True
      else:
       has_acc = True
      if has_acc:
       if int(access) > 30:
        reply(type, source, u'больше 30 нельзя!')
       elif int(access) < -5:
        reply(type, source, u'меньше -5 нельзя!')
       elif len(splitdata) == 1:
        if source[1] in CONFACCESS and jidto in CONFACCESS[source[1]]:
         change_conf_access(source[1], jidto)
        else:
         change_local_access(source[1], jidto)
        if source[1] not in POL_SEX.keys():
         reply(type, source, u'сняла доступ с "%s"' % (item))
        else:
         reply(type, source, u'снял доступ с "%s"' % (item))
       elif len(splitdata) == 2:
        change_local_access(source[1], jidto, int(access))
        if source[1] not in POL_SEX.keys():
         reply(type, source, u'для "%s" дала временно доступ: %s' % (item, access))
        else:
         reply(type, source, u'для "%s" дал временно доступ: %s' % (item, access))
       elif len(splitdata) == 3:
        change_conf_access(source[1], jidto, int(access))
        if source[1] not in POL_SEX.keys():
         reply(type, source, u'для "%s" дала навсегда доступ: %s' % (item, access))
        else:
         reply(type, source, u'для "%s" дал навсегда доступ: %s' % (item, access))
      else:
       reply(type, source, u'нет доступа!')
     else:
      reply(type, source, u'Это не жид, да и никого с таким ником я не знаю!')
    else:
     reply(type, source, u'Доступ, что ты пытаешься дать, не является числом!')
   else:
    reply(type, source, u'перебор параметров')
  else:
   reply(type, source, u'Чего ты от меня хочешь?')
 else:
  reply(type, source, u'ты не в чате!')

def handler_set_access_glob(type, source, Params):
 if Params:
  splitdata = Params.split()
  if len(splitdata) <= 2:
   item = splitdata[0].strip()
   if item.count('@') and item.count('.'):
    jid = item
   elif source[1] in GROUPCHATS and item in GROUPCHATS[source[1]]:
    jid = handler_jid(source[1]+'/'+item)
   else:
    jid = False
   if jid:
    if len(splitdata) == 2:
     access = splitdata[1].strip()
     if check_number(access):
      if access != '0':
       if jid not in ADLIST and int(access) >= 80:
        ADLIST.append(jid)
       change_global_access(jid, int(access))
       if source[1] not in POL_SEX.keys():
        reply(type, source, u'Для "%s" установила доступ: %s' % (item, access))
       else:
        reply(type, source, u'Для "%s" установил доступ: %s' % (item, access))
     else:
      reply(type, source, u'Доступ что ты пытаешся дать не является числом!')
    elif len(splitdata) == 1:
     if jid in GLOBACCESS:
      if jid in ADLIST:
       ADLIST.remove(jid)
      change_global_access(jid)
      if source[1] not in POL_SEX.keys():
       reply(type, source, u'Сняла доступ c "%s"' % (item))
      else:
       reply(type, source, u'Снял доступ c "%s"' % (item))
     else:
      reply(type, source, u'У "%s" и так нет глобального доступа!' % (item))
   else:
    reply(type, source, u'Это не жид да и никого с таким ником я незнаю!')
  else:
   reply(type, source, u'перебор параметров')
 else:
  reply(type, source, u'а дальше?')

def change_conf_access(conf, jid, level = 0):
 if conf not in CONFACCESS:
  CONFACCESS[conf] = {}
 if level:
  CONFACCESS[conf][jid] = level
 else:
  del CONFACCESS[conf][jid]
 write_file('dynamic/'+conf+'/access.txt', str(CONFACCESS[conf]))

def load_conf_access_levels(conf):
 if check_file(conf, 'access.txt'):
  CONFACCESS[conf] = eval(read_file('dynamic/'+conf+'/access.txt'))
 else:
  delivery(u'Внимание! Не удалось создать access.txt для "%s"!' % (conf))

command_handler(handler_set_access, 20, "access")
command_handler(handler_set_access_glob, 100, "access")

register_stage1_init(load_conf_access_levels)
