#===istalismanplugin===
# -*- coding: utf-8 -*-

# author ferym@jabbim.org.ru
# web sites - http://jabbrik.ru , http://veganet.org
# plugin version 1.5-testing

import os

def handler_note_add(type, source, parameters):
    if check_file('notepad','notepad.txt'):
      files = 'dynamic/notepad/notepad.txt'
      fp = open(files, 'r')
      note = eval(fp.read())
      fp.close()
      if parameters:
        if handler_jid(source[1]+'/'+source[2]) in note:
            if os.path.isfile('dynamic/notepad/limit.cfg'):
              lf = 'dynamic/notepad/limit.cfg'
              lr = open(lf, 'r')
              limit = eval(lr.read())
              lr.close()
              if len(note[handler_jid(source[1]+'/'+source[2])])>=limit:
                if limit==0:
                  reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                  return
                reply(type, source, u'Максимальное число хранимых записей - '+str(limit))
              else:
                dates = time.strftime('%H:%M:%S %d.%m.%y\n')
                note[handler_jid(source[1]+'/'+source[2])].append(dates+parameters)
                write_file(files, str(note))
                status='dnd'
                change_bot_status(source[1],u'Запись данных',status)
                time.sleep(5)
                message = STATUS[source[1]]['message']
                status = STATUS[source[1]]['status']
                change_bot_status(source[1], message, status)
                if source[1] not in POL_SEX.keys():
                  reply(type, source, u'Запомнила')
                else:
                  reply(type, source, u'Запомнил')
            else:
              lf = 'dynamic/notepad/limit.cfg'
              write_file(lf, str(25))
              lr = open(lf, 'r')
              limit = eval(lr.read())
              lr.close()
              if len(note[handler_jid(source[1]+'/'+source[2])])>=limit:
                if limit==0:
                  reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                  return
                reply(type, source, u'Максимальное число хранимых записей - '+str(limit))
              else:
                dates = time.strftime('%H:%M:%S %d.%m.%y\n')
                note[handler_jid(source[1]+'/'+source[2])].append(dates+parameters)
                write_file(files, str(note))
                status='dnd'
                change_bot_status(source[1],u'Запись данных......',status)
                time.sleep(5)
                message = STATUS[source[1]]['message']
                status = STATUS[source[1]]['status']
                change_bot_status(source[1], message, status)
                if source[1] not in POL_SEX.keys():
                  reply(type, source, u'Запомнила')
                else:
                  reply(type, source, u'Запомнил')
        else:
          if os.path.isfile('dynamic/notepad/limit.cfg'):
            lf = 'dynamic/notepad/limit.cfg'
            lr = open(lf, 'r')
            limit = eval(lr.read())
            lr.close()
            note[handler_jid(source[1]+'/'+source[2])] = []
            dates = time.strftime('%H:%M:%S %d.%m.%y\n')
            if limit==0:
              reply(type, source, u'Запись в блокнот временна отключена администратором бота')
              return
            note[handler_jid(source[1]+'/'+source[2])].append(dates+parameters)
            write_file(files, str(note))
            status='dnd'
            change_bot_status(source[1],u'Запись данных......',status)
            time.sleep(5)
            message = STATUS[source[1]]['message']
            status = STATUS[source[1]]['status']
            change_bot_status(source[1], message, status)
            if source[1] not in POL_SEX.keys():
              reply(type, source, u'Запомнила')
            else:
              reply(type, source, u'Запомнил')
          else:
            lf = 'dynamic/notepad/limit.cfg'
            write_file(lf, str(25))
            note[handler_jid(source[1]+'/'+source[2])] = []
            dates = time.strftime('%H:%M:%S %d.%m.%y\n')
            note[handler_jid(source[1]+'/'+source[2])].append(dates+parameters)
            write_file(files, str(note))
            status='dnd'
            change_bot_status(source[1],u'Запись данных......',status)
            time.sleep(5)
            message = STATUS[source[1]]['message']
            status = STATUS[source[1]]['status']
            change_bot_status(source[1], message, status)
            if source[1] not in POL_SEX.keys():
              reply(type, source, u'запомнила')
            else:
              reply(type, source, u'запомнил')
      else:
        reply(type, source, u'Что записать то?')
    else:
      reply(type, source, u'Ошибка в базе notepad!\nСрочно сообщите админу бота')
      
def handler_note_del(type, source, parameters):
  if check_file('notepad','notepad.txt'):
    files = 'dynamic/notepad/notepad.txt'
    fp = open(files, 'r')
    note = eval(fp.read())
    fp.close()
    if not parameters:
      reply(type, source, u'Не нахожу твоих записей')
      return
    if handler_jid(source[1]+'/'+source[2]) in note:
      try:
        parameters = int(parameters) - int(1)
        del note[handler_jid(source[1]+'/'+source[2])][parameters]
        write_file(files, str(note))
        status='dnd'
        change_bot_status(source[1],u'Удаление данных.....',status)
        time.sleep(5)
        message = STATUS[source[1]]['message']
        status = STATUS[source[1]]['status']
        change_bot_status(source[1], message, status)
        if source[1] not in POL_SEX.keys():
          reply(type, source, u'забыла')
        else:
          reply(type, source, u'забыл')
      except:
        reply(type, source, u'Не получилось')
    else:
      reply(type, source, u'Не нахожу твоих записей')
  else:
    reply(type, source, u'База notepad не создана. Сообщите админу бота')
    
def handler_note_show(type, source, parameters):
      if check_file('notepad','notepad.txt'):
        files = 'dynamic/notepad/notepad.txt'
        fp = open(files, 'r')
        note = eval(fp.read())
        fp.close()
        if not parameters:
          if handler_jid(source[1]+'/'+source[2]) in note:
            rep = ''
            for a, b in enumerate(note[handler_jid(source[1]+'/'+source[2])]):
              rep+=str(a+1)+') '+b+'\n'
            if str(note[handler_jid(source[1]+'/'+source[2])]) == '[]':
              reply(type, source, u'Не нахожу твоих записей')
              return
            reply(type, source, '\n'+rep)
          else:
            reply(type, source, u'Не нахожу твоих записей')
            return
        params = parameters.split(' ', 1)
        if len(params) == 1:
              if params[0]==u'clear':
                if handler_jid(source[1]+'/'+source[2]) in note:
                  del note[handler_jid(source[1]+'/'+source[2])]
                  write_file(files, str(note))
                  if source[1] not in POL_SEX.keys():
                    reply(type, source, u'Очистила список твоих записей')
                  else:
                    reply(type, source, u'Очистил список твоих записей')
                else:
                  reply(type, source, u'Не нахожу твоих записей')
              if params[0]==u'limit':
                if os.path.isfile('dynamic/notepad/limit.cfg'):
                  lf = 'dynamic/notepad/limit.cfg'
                  lr = open(lf, 'r')
                  lt = eval(lr.read())
                  lr.close()
                  if str(lt)=='0':
                    reply(type, source, u'Запись в блокнот временна отключена администратором бота')
                    return
                  reply(type, source, u'Установлен лимит записей - '+str(lt))
                else:
                  lf = 'dynamic/notepad/limit.cfg'
                  write_file(lf,str(25))
                  time.sleep(0.1)
                  lr = open(lf, 'r')
                  lt = eval(lr.read())
                  lr.close()
                  reply(type, source, u'Установлен лимит записей - '+str(lt))
        elif len(params) == 2:
            if params[0]==u'limit':
              if user_level(source[1]+'/'+source[2], source[1])==100:
                try:
                  if int(params[1])+int(1):
                    write_file('dynamic/notepad/limit.cfg',str(params[1]))
                    if params[1]==u'0':
                      reply(type, source, u'Запись в блокнот отключена')
                      return
                    reply(type, source, u'Установлен лимит записей - '+str(params[1]))
                except ValueError:
                  reply(type, source, u'Ты где такие цифры видел?')
              else:
                reply(type, source, u'Смена лимита доступна только админам бота')
            else:
              if handler_jid(source[1]+'/'+source[2]) in note:
                rep = ''
                for a, b in enumerate(note[handler_jid(source[1]+'/'+source[2])]):
                  rep+=str(a+1)+') '+b+'\n'
                if str(note[handler_jid(source[1]+'/'+source[2])]) == '[]':
                  reply(type, source, u'Не нахожу твоих записей')
                  return
                reply(type, source, '\n'+rep)
              else:
                reply(type, source, u'Не нахожу твоих записей')
                return
      else:
        reply(type, source, u'База notepad не создана. сообщите админу боту')
        
        
register_command_handler(handler_note_add, 'запомнить', ['mod','все','фан'], 10, 'Команда находится в плагине:\n54_note.py\nВаш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#добавляет запись в ваш личный блокнот', 'запомнить <что-то>', ['запомнить нужно посетить jabbrik.ru\nby ferym'])
register_command_handler(handler_note_del, 'забыть', ['mod','все','фан'], 10, 'Команда находится в плагине:\n54_note.py\nВаш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#Удаляет запись из вашего личного блокнота', 'забыть <номер записи>', ['забыть 2\nby ferym'])
register_command_handler(handler_note_show, 'записи', ['mod','все','фан'], 10, 'Команда находится в плагине:\n54_note.py\nВаш личный блокнотик. Всё введенные вами записи привязываются к вашему JID, доступно в любой конференции где сидит бот.\n#без параметра - Показывает все записи из вашего личного блокнота\nзаписи clear - очищает весь список ваших записей\nзаписи limit - просмотр установленного админом лимита на кол-во записей\nзаписи limit <число> - установка лимита записей, доступно админам бота', 'записи\nзаписи <parameters> <parameters>', ['записи\nзаписи clear\nзаписи limit\nзаписи limit 15\nby ferym'])