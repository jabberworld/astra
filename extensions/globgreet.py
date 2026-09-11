#===istalismanplugin===
# -*- coding: utf-8 -*-

GLOB_GREETEX = {}

def handler_globgreet(t, s, p):
        global GLOB_GREETEX
        if not p:
            jid = handler_jid(s[0])
            if jid in GLOB_GREETEX.keys():
                jid = handler_jid(s[0])
                del GLOB_GREETEX[jid]
                globgreet_save_now()
                reply(t, s, u'Глобальное приветствие удалено')
                return
            else:
                reply(t, s, u'И так нет глобального приветствия')
                return
        jid = handler_jid(s[0])
        if not jid in GLOB_GREETEX.keys():
            GLOB_GREETEX[jid] = p
            reply(t, s, u'Глобальное приветствие установлено!')
            globgreet_save_now()
        else:
            GLOB_GREETEX[jid] = p
            reply(t, s, u'Глобальное приветствие обновлено!')
            globgreet_save_now()

def globgreet_load_now(*list):
        global GLOB_GREETEX
        try:
                fp = file('dynamic/globgreet.txt', 'r')
                GLOB_GREETEX = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/globgreet.txt', 'w')
                GLOB_GREETEX = {}
                fp.write( str(GLOB_GREETEX) )
                fp.close()

def globgreet_save_now():
        global GLOB_GREETEX
        fp = file('dynamic/globgreet.txt', 'w')
        fp.write( str(GLOB_GREETEX) )
        fp.close()

def join_globgreet(conf, nick, afl, role):
        jid = handler_jid(conf+'/'+nick)
        if jid in GLOB_GREETEX.keys():
            msg(conf, '%s, %s' % (nick, str.join('',GLOB_GREETEX[jid])))
        else:
            return

register_join_handler(join_globgreet)

register_stage1_init(globgreet_load_now)
register_command_handler(handler_globgreet, 'глобпривет', ['доступ','все'], 10, 'Команда находится в плагине:\nglobgreet.py\nУстанавлиыает глобальное приветствие! Без параметров - удаляет.', 'глобпривет текст', ['глобпривет Категорически приветствую Кота'])