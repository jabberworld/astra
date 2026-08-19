#===istalismanplugin===
# -*- coding: utf-8 -*-

A_NAME = {}
A_SITY = {}
A_HORO = {}


def anketa(type, source, body):
   global A_NAME
   global A_SITY
   global A_HORO
   repl = u'~*~ Ваша Анкета:'
   jid = handler_jid(source[0])
   if jid in A_NAME.keys():
      repl += u'\n~*~ Имя: '+str.join('',A_NAME[jid])
   else:
      repl += u'\n~*~ Имя: ---'
   if jid in A_SITY.keys():
      repl += u'\n~*~ Город: '+str.join('',A_SITY[jid])
   else:
      repl += u'\n~*~ Город: ---'
   if jid in A_HORO.keys():
      repl += u'\n~*~ Зодиак: '+str.join('',A_HORO[jid])
   else:
      repl += u'\n~*~ Зодиак: ---'
   reply(type,source,repl)

register_command_handler(anketa, 'анкета', [], 10, 'Ваша анкета, содержит несколько параметров:\nИмя - меняет обращение бота к Вам\nГород - служит для команды погода, показывает прогноз погоды исходя из данных анкеты.\nЗодиак - служит для команды гороскоп, показывает гороскоп исходя из данных анкеты', 'имя ваше_имя', ['город Ростов-на-Дону'])

def ahoro_load_now(*list):
        global A_HORO
        try:
                fp = file('dynamic/ahoro.txt', 'r')
                A_HORO = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/ahoro.txt', 'w')
                A_HORO = {}
                fp.write( str(A_HORO) )
                fp.close()

def asity_load_now(*list):
        global A_SITY
        try:
                fp = file('dynamic/asity.txt', 'r')
                A_SITY = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/asity.txt', 'w')
                A_SITY = {}
                fp.write( str(A_SITY) )
                fp.close()

def handler_asity(t, s, p):
        global A_SITY
        if not p:
            jid = handler_jid(s[0])
            if jid in A_SITY.keys():
                del A_SITY[jid]
                reply(t, s, u'Пунк город очищен!')
                asity_save_now()
                return
            else:
                reply(t, s, u'И так не установлено!')
                return
        jid = handler_jid(s[0])
        if not jid in A_SITY.keys():
            A_SITY[jid] = p
            reply(t, s, u'Добавлено')
            asity_save_now()
        else:
            A_SITY[jid] = p
            reply(t, s, u'Обновлено!')
            asity_save_now()

def handler_a_horo(t, s, p):
        if not p:
            global A_HORO
            jid = handler_jid(s[0])
            if jid in A_HORO.keys():
                del A_HORO[jid]
                reply(t, s, u'Пунк знак зодиака очищен!')
                ahoro_save_now()
                return
            else:
                reply(t, s, u'И так не установлено!')
                return
        jid = handler_jid(s[0])
        if not jid in A_HORO.keys():
            A_HORO[jid] = p
            reply(t, s, u'Добавлено')
            ahoro_save_now()
        else:
            A_HORO[jid] = p
            reply(t, s, u'Обновлено!')
            ahoro_save_now()

register_command_handler(handler_a_horo, 'зодиак', [], 10, 'Добавляет в анкету ваш знак зодиака, служит для команды гороскоп, показывает гороскоп исходя из данных в анкете.', 'зодиак лев', ['зодиак лев'])

register_command_handler(handler_asity, 'город', [], 10, 'Добавляет в анкету ваш город, служит для команды погода, показывает погоду в городе исходя из данных анкеты.', 'город Ростов', ['город Москва'])

def handler_aname(t, s, p):
        if not p:
            global A_NAME
            jid = handler_jid(s[0])
            if jid in A_NAME.keys():
                del A_NAME[jid]
                reply(t, s, u'Обращение удалено')
                a_save_now()
                return
            else:
                reply(t, s, u'И так не установлено!')
                return
        jid = handler_jid(s[0])
        if not jid in A_NAME.keys():
            if len(p) <= 20:
                if p not in COMMANDS:
                    if p.count(' '):
                        reply(t, s, u'Пробеллы запрещены')
                        return
                    A_NAME[jid] = p
                    reply(t, s, u'Оч приятно :)')
                    a_save_now()
                else:
                    reply(t, s , u'Нельзя так как это команда')
            else:
                reply(t, s, u'В обращении не более 20 символов!!!')
        else:
            if len(p) <= 20:
                if p not in COMMANDS:
                    if p.count(' '):
                        reply(t, s, u'Пробеллы запрещены')
                        return
                    A_NAME[jid] = p
                    reply(t, s, u'Шо это ты решил переименоватцо?')
                    a_save_now()
                else:
                    reply(t, s , u'Нельзя так как это команда')
            else:
                reply(t, s, u'В обращении не более 20 символов!!!')

def a_load_now(*list):
        global A_NAME
        try:
                fp = file('dynamic/aname.txt', 'r')
                A_NAME = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/aname.txt', 'w')
                A_NAME = {}
                fp.write( str(A_NAME) )
                fp.close()

def ahoro_save_now():
        global A_HORO
        fp = file('dynamic/ahoro.txt', 'w')
        fp.write( str(A_HORO) )
        fp.close()

def asity_save_now():
        global A_SITY
        fp = file('dynamic/asity.txt', 'w')
        fp.write( str(A_SITY) )
        fp.close()

def a_save_now():
        global A_NAME
        fp = file('dynamic/aname.txt', 'w')
        fp.write( str(A_NAME) )
        fp.close()

#register_command_handler(afools_control, 'afools', [], 30, '','',[''])

def afools_control(t,s,p):
   if p == u'вкл':
      if s[1] not in AFOOLS.keys():
         AFOOLS[s[1]] = 1
         fp = file('dynamic/afools.txt', 'w')
         fp.write( str(AFOOLS) )
         fp.close()
         reply(t,s,u'ok')
         return
      else:
         reply(t,s,u'и так включено')
         return
   if p == u'выкл':
      if s[1] in AFOOLS.keys():
         del AFOOLS[s[1]]
         fp = file('dynamic/afools.txt', 'w')
         fp.write( str(AFOOLS) )
         fp.close()
         reply(t,s,u'ok')
         return
      else:
         reply(t,s,u'и так выключено')
         return
   else:
      if s[1] not in AFOOLS.keys():
         reply(t,s,u'Выключено')
         return
      else:
         reply(t,s,u'включено')
         return

register_command_handler(afools_control, 'afools', [], 30, '','',[''])

def afools_load_now(*list):
        global AFOOLS
        try:
                fp = file('dynamic/afools.txt', 'r')
                AFOOLS = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/afools.txt', 'w')
                AFOOLS = {}
                fp.write( str(AFOOLS) )
                fp.close()

register_stage1_init(afools_load_now)
register_stage1_init(ahoro_load_now)
register_stage1_init(asity_load_now)
register_stage1_init(a_load_now)
register_command_handler(handler_aname, 'имя', ['доступ','все'], 10, 'Команда находится в плагине:\nname.py\nПоменять обращение бота для себя.', 'имя Олег', ['имя Чувак'])