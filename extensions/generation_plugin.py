#===istalismanplugin===
# -*- coding: utf-8 -*-
# From Mr.King [new_jabber_bots@conference.jabber.ru]
def pass2(type, source, parameters):
        pass2=[u'1',u'2','3','4','5','6','7','8','9','0','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',u'1',u'2','3','4','5','6','7','8','9','0', u'Q', u'W',u'E', u'R', u'T', u'Y', u'U',u'I',u'O',u'P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M',u'1',u'2','3','4','5','6','7','8','9','0',u'1',u'2','3','4','5','6','7','8','9','0']
        pass_to_nick=u'Вот тебе пароль: '                
        if parameters:
                parol=int(parameters)
        else:
                parol=5
        if int(parol)< 4:
                reply(type, source, u'Такой простой пароль не буду делать!')
                return
        if int(parol)> 400:
                reply(type, source, u'Нихуя себе парольчик захотел о_О')
                return
        for x in range(0, parol):
                pass_to_nick+=random.choice(pass2)
        reply(type, source,pass_to_nick)
register_command_handler(pass2, 'ген', ['кинг', 'все'], 10, 'Генератор паролей\nВерсия плагина: 1.2\nFrom Mr.King', 'ген <nomer>', ['ген 2', 'ген 10'])
