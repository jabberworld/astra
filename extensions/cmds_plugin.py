#===istalismanplugin===
# -*- coding: utf-8 -*-

# Coded by: Avinar  (avinar@xmpp.ru)

# licence show in another plugins ;)



def handler_some_commands(type, source, parameters):
        if parameters:
                args = parameters.split(';')
                if len(args) > 20:
                        reply(type, source, u'Сликом много подкоманд. максимум 20.')
                        return
                for body in args:
                        try:
                                body=body.strip()
                                command,cparameters,cbody,rcmd = '','','',''
                                rcmd = body.split(' ')[0].lower()
                                if not body:
                                        reply(type, source,  u'Пустая подкоманда. проверьте правильность написания')
                                        time.sleep(1)
                                        continue
                                if body.count('%SLEEP1%'):
                                        time.sleep(1)
                                        continue
                                if body.count('%SLEEP2%'):
                                        time.sleep(2)
                                        continue
                                if body.count('%SLEEP3%'):
                                        time.sleep(3)
                                        continue
                                if body.count('%SLEEP10%'):
                                        time.sleep(10)
                                        continue					
                                if body.count('%SLEEP60%'):
                                        time.sleep(60)
                                        continue						
                                                
                                body=body.replace('%NICK%',source[2]).replace('%CONF%',source[1])
                                        
                                real_access = MACROS.get_access(rcmd, source[1])
                                if real_access < 0:
                                        real_access = COMMANDS[rcmd]['access']
                                if real_access > 30:
                                        reply(type, source,  u'Нетушки. непрокатит ;)')
                                        time.sleep(1)
                                        continue
                                        
                                cbody = MACROS.expand(body, source)
                                command=cbody.split()[0].lower()
                                if cbody.count(' '):
                                        cparameters = cbody[(cbody.find(' ') + 1):].strip()
                                if command in COMMANDS:
                                        with smph:
                                                INFO['thr'] += 1
                                                threading.Thread(None,COMMAND_HANDLERS[command],'command'+str(INFO['thr']),(type, source, cparameters,)).start()
                                                time.sleep(1)
                                else:
                                        reply(type, source,  u'Неправильная команда. Проверьте правильность написания')
                                        time.sleep(1)
                                        continue
                        except:
                                reply(type, source,  u'Неправильная команда внутри .ком ;)')
                                time.sleep(1)
        else:
                reply(type, source, u'нет внутренних подкомманд.')
        return


        
        
def handler_null_commands(type, source, parameters):
        if parameters:
                try:
                                body=parameters.strip()
                                command,cparameters,cbody,rcmd = '','','',''
                                rcmd = body.split(' ')[0].lower()
                                if not body:
                                        reply(type, source,  u'Пустая подкоманда в нулл. проверьте правильность написания')
                                        return
                                        
                                real_access = MACROS.get_access(rcmd, source[1])
                                if real_access < 0:
                                        real_access = COMMANDS[rcmd]['access']
                                if real_access > 30:
                                        reply(type, source,  u'Нетушки. непрокатит ;)')
                                        return
                                        
                                cbody = MACROS.expand(body, source)
                                command=cbody.split()[0].lower()
                                if cbody.count(' '):
                                        cparameters = cbody[(cbody.find(' ') + 1):].strip()
                                if command in COMMANDS:
                                        with smph:
                                                INFO['thr'] += 1
                                                threading.Thread(None,COMMAND_HANDLERS[command],'command'+str(INFO['thr']),('none', source, cparameters,)).start()
                                else:
                                        reply(type, source,  u'Неправильная команда в нулл. Проверьте правильность написания')
                                        return
                except:
                        reply(type, source,  u'Упс, ошибка в нулл.')
                        print('error in NULL')
        else:
                reply(type, source, u'нет внутренних подкомманд в нулл.')
        return	
        





#register_command_handler(handler_some_commands, '.ком', ['все'], 20, 'Добавить серию команд. команды будут выполнены по очереди (аналогично .commands у FreQ) Частенько используется в акмд или макросах.\nпеременные: \n%SLEEP1% задержка на 1 сек (В конференции есть такое понятие как "лимит сообщений" (Примерно одно сообщение - 1 секунда) поэтому если бот что-то говорит рекомендую делать задержки между фразами.\n%SLEEP2% и %SLEEP3% соответственно пауза на 2 и 3 секунды\n %NICK% возвращяет ник написавшего', '.ком <команда1>;<команда2>;<командаN>', ['.ком сказать /me проставляется;%SLEEP1%;водка всем','.алиас адд @conference.=.ком null кик %NICK% Рекламщик, не возвращяйся сюда!;null чисти'])

register_command_handler(handler_null_commands, 'нулл', ['все'], 100, 'Добавить такую команду, результат которой не будет выдан пользователюнулю (аналог .null у FreQ) ', 'нулл <команда>', ['нулл чисти','нулл кик Вася'])
register_command_handler(handler_null_commands, '!нулл', ['все'], 20, 'Добавить такую команду, результат которой не будет выдан пользователюнулю (аналог .null у FreQ) ', '!нулл <команда>', ['!нулл чисти','!нулл кик Вася'])
