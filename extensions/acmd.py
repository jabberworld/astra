#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Endless bot plugin v1.2

# Coded by: Avinar (avinar@xmpp.ru)
# http://jabrvista.net.ru

# licence show in another plugins ;)

acmds={}

def handler_acmd_add(type, source, parameters):
 global acmds
 parameters=parameters.strip()
 if not parameters.count('='):
  reply(type, source, u'ииии?')
  return
 groupchat=source[1]
 try:
  key = parameters.split('=')[0].strip().lower()
  if key=='':
   reply(type, source,  u'Пустое ключевое слово, проверь синтаксис ;)')
   return   
  srs=parameters[(parameters.find('=') + 1):].strip()
  if srs=='':
   reply(type, source,  u'Пустая внутренняя команда, проверь синтаксис ;)')
   return

  comma=srs.split(' ')[0].lower()
 except:
#  traceback.print_exc()
  reply(type, source,  u'Ты хоть сам понимаешь что от меня хочешь? ;)')
  return
 
 try:
  real_access = COMMANDS[comma]['access']
  if real_access > 30:
   reply(type, source,  u'Нетушки. Непрокатит ;)')
   return
 except:
#  traceback.print_exc()
  reply(type, source,  u'Неправильная команда внутри .алиаса ;)')
  return
 
 if MACROS.expand(key, source).split()[0] in globals()['COMMANDS']:
  reply(type, source,  u'Такая команда уже существует! ;)') 
  return
 
 global acmds 
 DBPATH='dynamic/'+groupchat+'/acmd.txt'
 if check_file(groupchat,'acmd.txt'):
  localdb = load_file(DBPATH, {})
  localdb[key] = srs
  write_file(DBPATH, str(localdb))
  if not groupchat in acmds:
   acmds[groupchat]={}
  acmds[groupchat][key] = srs
  status='dnd'
  change_bot_status(source[1],u'Сохраняю.....',status)
  time.sleep(5)
  message = STATUS[source[1]]['message']
  status = STATUS[source[1]]['status']
  change_bot_status(source[1], message, status)
  if source[1] not in POL_SEX.keys():
   reply(type, source, u'Добавила')
  else:
   reply(type, source, u'Добавил')
 else:
  reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')

  
def handler_acmd_show(type, source, parameters):
 global acmds
 groupchat=source[1]
 if groupchat in acmds:
  z=0
  num=len(acmds[groupchat].keys())
  if num != 0:
   message1=u'.алиас лист: \n'
   for x in acmds[groupchat].keys():
    z+=1
    message1 += str(z)+') ' + x + '=' + acmds[groupchat][x] + '\n'
   if z==1:
    ss=u' пункт.'
   elif z>1 and z<5:
    ss=u' пункта.'
   else:
    ss=u' пунктов.'
   status='dnd'
   change_bot_status(source[1],u'Получаю список.....',status)
   time.sleep(5)
   message = STATUS[source[1]]['message']
   status = STATUS[source[1]]['status']
   change_bot_status(source[1], message, status)
   reply(type, source, message1 + u'Всего ' + str(z) + ss)
   return
  else:
   reply(type, source, u'В вашей конференции нету .алиасов!')
   return   
 else:
  reply(type,source,u'В вашей конференции нету .алиасов!')
  return

  
def handler_acmd_del(type, source, parameters):
 global acmds
 groupchat=source[1]
 parameters=parameters.strip().lower()
 if parameters=='':
  reply(type, source, u'Ииии?')
  return
 if groupchat in acmds:
  if parameters in acmds[groupchat]:
   del acmds[groupchat][parameters]
   DBPATH='dynamic/'+groupchat+'/acmd.txt'
   if check_file(groupchat,'acmd.txt'):
    localdb = load_file(DBPATH, {})
    if parameters.strip() in localdb:
     del localdb[parameters.strip()]
     write_file(DBPATH, str(localdb))
    
   status='dnd'
   change_bot_status(source[1],u'Удаляю.....',status)
   time.sleep(5)
   message = STATUS[source[1]]['message']
   status = STATUS[source[1]]['status']
   change_bot_status(source[1], message, status)
   if source[1] not in POL_SEX.keys():
    reply(type, source, u'Удалила!')
   else:
    reply(type, source, u'Удалил')
  else:
   reply(type, source,  u'Нет такого .алиаса, просмотри сначала ".алиас лист" ;)')
 else:
  reply(type,source,u'База пуста')

  
def handler_acmd_clear(type, source, parameters):
 global acmds
 groupchat=source[1]
 parameters=parameters.strip().lower()
 DBPATH='dynamic/'+groupchat+'/acmd.txt'
 if check_file(groupchat,'acmd.txt'):
  write_file(DBPATH, '{}')

 if groupchat in acmds:
  del acmds[groupchat]
  if source[1] not in POL_SEX.keys():
   reply(type, source, u'Очистила :(')
  else:
   reply(type, source, u'Очистил')
 else:  
  reply(type,source, u'База .алиасов пуста.')


def handler_acmd_msg(raw, type, source, parameters):
 global acmds
 if parameters.lower().strip().count(u'акмд'):
  return
 if source[1] not in GROUPCHATS.keys():
  return
 
 if source[1] not in acmds.keys(): 
  return
#   DBPATH='dynamic/'+source[1]+'/acmd.txt'
#   if check_file(source[1],'acmd.txt'):
#    localdb = load_file(DBPATH, {})
#    acmds[source[1]]=localdb
    
 parameters=parameters.lower().strip()
 for word in acmds[source[1]].keys():
  if parameters.count(word):
   try:
    cbody = acmds[source[1]][word]
    if len(cbody.split(' ')) == 1:
     comma = cbody.lower()
     params = ''
    else:
     comma = cbody.split(' ')[0].lower()
     params = cbody[(cbody.find(' ') + 1):].strip()
    
#    if params.count('%NICK%'):
    params=params.replace('%NICK%',source[2]).replace('%CONF%',source[1])
    
    real_access = MACROS.get_access(cbody, source[1])
    if real_access < 0:
     real_access = COMMANDS[comma]['access']
    if real_access > 30:
     reply(type, source,  u'Фиг!') 
     return
   except:
#    traceback.print_exc()
    reply(type, source,  u'Неправильная команда внутри .алиаса.')
    return
   
   INFO['thr'] += 1
   with smph:
    threading.Thread(None,COMMAND_HANDLERS[comma],'command'+str(INFO['thr']),(type, source, params,)).start()


def handler_acmd_call(type, source, parameters):
 if parameters:
  
#  if not check_file(source[1],'acmd.txt'):
#   write_file(DBPATH, u'{}')
#  if not source[1] in acmds.keys():
#   acmds[source[1]] = load_file(DBPATH, {})
  
  if len(parameters.split(' ')) > 1:
   actype=parameters.split()[0].lower()
   acparams = parameters[(parameters.find(' ') + 1):].strip()
  else:
   actype=parameters.lower().strip()
   acparams=''
  
  if actype == 'add' or actype == u'адд':
   handler_acmd_add(type, source, acparams)
   return
  elif actype == 'del' or actype == u'дел':
   handler_acmd_del(type, source, acparams)
   return
  elif actype == 'list' or actype == u'лист':
   handler_acmd_show(type, source, acparams)
   return
  elif actype == 'clear' or actype == u'очистить':
   handler_acmd_clear(type, source, acparams)
   return
  elif actype == 'help' or actype == u'помощь':
   reply(type, source, u'.алиасы сделаны с закосом под !muc acmd у бота Gluxi. \nпримеры: \n  .алиас адд прячьтесь=сказать /me спрятался\n  .алиас адд висю=пинг\n(в данном случае команды выполняется от имени сказавшего "пинг") \n  .алиас лист\n  .алиас дел прячьтесь\n\nпосле знака = стоит обычная команда талисмана. \nДотступен параметр %NICK% и %CONF%')
  else:
   handler_acmd_add(type, source, parameters)
 else:
  reply(type, source, u'Почитай "помощь .алиас" ;)')
  return
  

def acmd_init(groupchat): 
 global acmds
 DBPATH='dynamic/'+groupchat+'/acmd.txt'
 if check_file(groupchat,'acmd.txt'):
  localdb = load_file(DBPATH, {})
  num=len(localdb.keys())
  if num:  
   acmds[groupchat]=localdb

  
register_command_handler(handler_acmd_call, '.алиас', ['акмд','все'], 20, 'Команда находится в плагине:\nacmd.py\nАкоманды. доступные параметры:\n помощь, адд, дел, лист, очистить. ', '.алиас [параметр] [<слово>][=<команда>]', ['.алиас помощь','.алиас чмок=сказать /me пацеловал %NICK% взасос!','.алиас дел чмок'])

register_message_handler(handler_acmd_msg)

register_stage1_init(acmd_init)

#register_command_handler(handler_acmd_add, 'acmd_add', ['акмд'], 20, 'Добавить акоманду! \nFrom Mr.King', 'acmd_add <слов>=<значение>', ['acmd_add привет=сказать привет!'])
#register_command_handler(handler_acmd_show, 'acmd_show', ['акмд'], 10, 'показать список акоманд!\nFrom Mr.King', 'acmd_show', ['acmd_show'])
#register_command_handler(handler_acmd_del, 'acmd_del', ['акмд'], 20, 'Удалить акоманду\nFrom Mr.King', 'acmd_del <слово>', ['acmd_del привет'])

