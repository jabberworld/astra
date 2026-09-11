#===istalismanplugin===
# -*- coding: utf-8 -*-

ZVANIE = {}

def zvanie_add(t,s,b):
    jid1 = b.split()[0]
    if not jid1 in ZVANIE.keys():
        jid1 = b.split()[0]
        ZVANIE[jid1] = {}
    ZVANIE[jid1] = b.split()[1]
    save_zvanie()
    reply(t,s,u'Добавлено')

def zvanie_del(t,s,b):
    jid1 = b.split()[0]
    if jid1 in ZVANIE.keys():
        del ZVANIE[jid1]
        save_zvanie()
        reply(t,s,u'Удалено')
    else:
        reply(t,s,u'Не установлено')

register_command_handler(zvanie_del, 'звание-', [], 100, '', '', [''])

register_command_handler(zvanie_add, 'звание+', [], 100, 'Дает юзеру звание.', 'заание+ жид число', ['звание+ user@jabber.ru 1'])

def save_zvanie():
    global ZVANIE
    fp = file('dynamic/zvanie.txt', 'w')
    fp.write( str(ZVANIE) )
    fp.close()

def load_zvanie(*list):
        global ZVANIE
        try:
                fp = file('dynamic/zvanie.txt', 'r')
                ZVANIE = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/zvanie.txt', 'w')
                ZVANIE = {}
                fp.write( str(ZVANIE) )
                fp.close()

register_stage1_init(load_zvanie)

def zvanie_work(conf, nick, afl, role):
    jid = handler_jid(conf+'/'+nick)
    if jid in ZVANIE.keys():
        if ZVANIE[jid] == '1':
            msg(conf, u'/me приветствует флудераста '+nick)
            return
        elif ZVANIE[jid] == '2':
            msg(conf, u'/me приветствует почетного флудераста '+nick)
            return
        elif ZVANIE[jid] == '3':
            msg(conf, u'/me приветствует мразь '+nick)
            return
        elif ZVANIE[jid] == '4':
            msg(conf, u'/me приветствует быдло '+nick)
            return
        else:
            return
    else:
        return

register_join_handler(zvanie_work)
