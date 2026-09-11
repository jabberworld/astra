# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  help_plugin.py

# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/


def hnd_cmd_guide(t, s, p):
        rep = ''
        i = sorted(COMMANDS.keys())
        for x in i:
                try: a = COMMANDS[x]['desc']
                except: continue
                if len(a)>80:
                        a = a[:80]+'...'
                rep+= x+' - '+a+'\n'
        reply(t, s, u'Всего команд '+str(len(COMMANDS.keys()))+u':\n'+rep)

register_command_handler(hnd_cmd_guide, 'комгид', ['хелп','инфо','все'], 0, 'Выводит все команды и краткое описание к ним.', 'комгид', ['комгид'])

HELP_TIME = {}

def command_comaccess(type,source,body):
        if body:
                command = body.lower()
                if command in COMMANDS:
                        access = COMMANDS[command]['access']
                        reply(type, source, u'Доступ к команде "'+command+'" = '+str(access))
                else:
                        reply(type, source, u'нет такой команды')
        else:
                reply(type, source, u'Команды "None" не существует! lol')

def command_help(type, source, body):
        if body:
                command = body.lower()
                if len(command) <= 24:
                        if command in COMMANDS:
                                try:
                                        if 'desc' in COMMANDS[command]:
                                                fr = COMMANDS[command]
                                        else:
                                                plug = COMMANDS[command]['plug']
                                                inst = COMMAND_HANDLERS[command].__name__
                                                fr = load_file("help/%s" % plug, {})[inst]
                                        mess = fr['desc']
                                        mess += u'\nИспользование: '+fr['syntax']+u'\nПримеры:'
                                        for example in fr['examples']:
                                                mess += '\n  >>>>>  '+example
                                        mess += u'\nНеобходимый уровень доступа: '+str(COMMANDS[command]['access'])
                                        reply(type,source,mess)
                                except:
                                        reply(type,source,u'нет хелпа')
                        else:
                                reply(type,source,u'Нет такой команды, чтобы узнать точный список напиши "команды"')
                else:
                        reply(type,source,u'Команды длинне 24х символов точно не существует! ЛОЛ')
        else:
                 HELP_TIME[source[1]] = 1
                 reply(type,source,u'✯✯✯ Вы находитесь в меню справки, выберите действие:\n ☞ 1 - Команды бота;\n ☞ 2 - список макро;\n ☞ 3 - Подробная справка;\n ☞ 4 - О боте;\n ☞ 5 - Создание своих команд;\n ☞ 6 - Тамагочи;\n ☞ 7 - Адрес конференции поддержки бота;\n ☞ 8 - Написать ботоводу;\n ☞ 0 - Выход.\n✯✯✯')
                 if source[1] in HELP_TIME.keys():
                          register_command_handler(command_comlist2, '1', [], 10, '', '', [''])
                          register_command_handler(macrolist_handler11, '2', [], 10, '', '', [''])
                          register_command_handler(spravka_help, '3', [], 10, '', '', [''])
                          register_command_handler(o_bot, '4', [], 10, '', '', [''])
                          register_command_handler(svoi_commands, '5', [], 10, '', '', [''])
                          register_command_handler(tamagochi, '6', [], 10, '', '', [''])
                          register_command_handler(off_confa, '7', [], 10, '', '', [''])
                          register_command_handler(help_project, '8', [], 10, '', '', [''])
                          register_command_handler(help_exit, '0', [], 10, '', '', [''])
                          if source[1] in HELP_TIME.keys():
                                   time.sleep(120)
                                   help_exit(type,source,body)
                          else:
                                   return
                 else:
                          reply(type,source,u'Справка и так открыта!')

def spravka_help(type, source, body):
   reply(type,source,u'Приветствую тебя пользователь :-) ,\n Для получения справки по использованию команды, пиши "помощь <команда>".\n Пригласить админа бота в конфу можно командой "босса". Оставить заявку на установку этого бота в вашу конференцию можно по такой схеме:\n !админу установите бота в адрес_вашей_конфы')

def o_bot(type,source,body):
   reply(type,source,u'Астра - это слегка модифицированый бот BlackSmith mark 1. r131(Astra v8). Функционал бота достаточно широк как и для администрирования jabber конференций так и для развлечений(викторина, миллионер, 21очко, снежки, морской бой, рулетка, анекдоты, гороскоп, абсурд, лурк и т.д.) При необходимости бот может писать логи конференций (подробнее "помощь логгер"), благодаря мук-фильтру бот может фильтровать сообщения до того как они попадут в чат, а так же защищает вашу конференцию от спама и вайп атак, подробнее "помощь мук", в конфигураторе конференции должен быть прописан жид бота с ресурсом. Настоятельно рекомендую перед использованием незнакомой вам команды ознакомится со справкой по команде.')

def svoi_commands(type,source,body):
   reply(type,source,u'Команды которые позволяют добавлять ваши собственные: "макро", "алиас", ".алиас", "*".\n "МАКРО" - содержит дополнительные параметры, %(context, nick) - возвращает ник написавшего, %(context, conf) - возвращает конференцию, %(rand, m, n) - выбор числа от m - например 5 до n - например 10, все остальное можно узнать из справки по команде.\n Алиас - тот же набор инструментов для создания своих команд, но имеет более простой синтаксис, важно знать что команды созданные через алиас имеют уровень доступа 10, очень удобны для сокращений основных команд например "версия", "алиас !в=версия".\n .алиас - не менее интересный инструмент, особенность его в том что бот реагирует на "слова" и "словосочетания", для примера ".алиас адд олега позови=призвать олег", то есть бот в данном случае реагирует на два слова, ну а там ваша фантазия.\n "*" - это команда позволяет выполнять до четырех команд одновременно. Внимательно читаем справку по использованию этих команд.')

def tamagochi(type,source,body):
   reply(type,source,u'Что это наверняка все знают и у многих он был, сейчас есть возможность завести в своем чате своего тамагочика. И так. Тамагочи 1 - запуск тамагочика. СОСТОЯНИЕ - показывает общее состояние тамагочика, голод, жажду и прочее, в зависимости от состояния тамагочик меняет свое поведение, если состояние голода близко к нулю, тамагочик начинает просить кушать, так же с остальными параметрами состояния., параметер Интеллект - показывает развитие тамагочика, чем выше интеллект, тем больше параметров доступно. КУШАЙ - утолить голод, ПЕЙ - утолить жажду, доступная еда и напитки по команде ХОЛОДИЛЬНИК. ИГРАЙ - повышает отдых тамагочика. ГИГИЕНА - повышает гигиену. ПОЧИТАЙ - повышает интеллект. ЭНЕРГИЯ - расходуется в зависимости от частоты использования команд бота, ПОЙДИ СПАТЬ - отправляет тамагочика в сон, тем самым повышая его энергию. КОИНСЫ - виртуальная валюта тамагочика, расходуется от покупки тамагочику продуктов, пополнить коинсы можно играя с тамагочиком в игру ЧИСЛО и СТРАТЕГИЯ. Если у вас в чате недостаточно коинсов и бот не может покушать или попить, тогда тратиться здоровье. ВЫПЕЙ ВИТАМИНКУ - повышает здоровье тамагочика на 5 пунктов.')

def off_confa(type,source,body):
   msg(source[0],u'obshenie@conference.jabber.ru')

def help_project(type,source,body):
   reply(type,source,u'email: saranskcity@gmail.com')

def help_exit(type,source,body):
   if source[1] in HELP_TIME.keys():
      handler_command_out1(type, source, '1')
      handler_command_out1(type, source, '2')
      handler_command_out1(type, source, '3')
      handler_command_out1(type, source, '4')
      handler_command_out1(type, source, '5')
      handler_command_out1(type, source, '6')
      handler_command_out1(type, source, '7')
      handler_command_out1(type, source, '8')
      handler_command_out1(type, source, '0')
      del HELP_TIME[source[1]]
      reply(type,source,u'Вышла из справки.')
   else:
      return

def command_commands(type, source, body):
   if body == u'чат':
           answer = u"\nСписок команд в категории ✌все✌ (всего %d штук):\n\n%s." % (len(COMMANDS.keys()), " • ".join(sorted(COMMANDS.keys())))
           if len(COMMOFF.get(source[1], [])):
                   answer += u"\n\nСледующие команды здесь отключены: \n%s." % " • ".join(sorted(COMMOFF.get(source[1], [])))
           answer += u"\n\n✯✯✯ Чтобы узнать доступ к определённой команде, напишите \"комдоступ [команда]\"."
           if PREFIX.get(source[1]):
                   answer += u"\n✯✯✯ Префикс команд: \"%s\"." % PREFIX.get(source[1])
#	if type != "private":
#		reply(type, source, u"В привате.")	
           reply(type, source, answer)
   if not body:
           answer = u"\nСписок команд в категории ✌все✌ (всего %d штук):\n\n%s." % (len(COMMANDS.keys()), " • ".join(sorted(COMMANDS.keys())))
           if len(COMMOFF.get(source[1], [])):
                   answer += u"\n\nСледующие команды здесь отключены: \n%s." % " • ".join(sorted(COMMOFF.get(source[1], [])))
           answer += u"\n\n✯✯✯ Чтобы узнать доступ к определённой команде, напишите \"комдоступ [команда]\"."
           if PREFIX.get(source[1]):
                   answer += u"\n✯✯✯ Префикс команд: \"%s\"." % PREFIX.get(source[1])
           if type != "private":
                   reply(type, source, u"В привате.")	
           msg(source[0], answer)
           return
   if not body in ['чат']:
      reply(type,source,u'Непонятно :( попробуй написать просто "команды" или "команды чат" если приват закрыт.')
      return


command_handler(command_comaccess, 10, "help")
command_handler(command_help, 10, "help")
#(command_comlist, 10, "help")
command_handler(command_commands, 10, "help")
register_command_handler(command_help, 'помощь', [], 10, 'Дает основную справку или показывает справку к определленной команде, с параметром чат, выведет справку в чате.', '\n > хелп \n > ? \n > помощь', ['?','? пинг'])
register_command_handler(command_help, '?', [], 10, ' Дает основную справку или показывает справку к определленной команде, с параметром чат, выведет справку в чате.', '\n > хелп \n > ? \n > помощь ', ['?','? пинг'])
