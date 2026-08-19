#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Endless bot plugin v1.0

# Coded by: Avinar (avinar@xmpp.ru)
# http://jabrvista.net.ru

# licence show in another plugins ;)


def handler_gdeya(type, source, parameters):
        ms=u'№) {конфа} [ник в конфе] (число людей)'
        n=0
        for groupchat in GROUPCHATS.keys():
                n+=1
                users=len(GROUPCHATS[groupchat].keys())
                bnick=handler_botnick(groupchat)
                ms+='\n'+str(n)+') '+  groupchat + ' [' + bnick + '] ('+str(users)+')'
                
        reply(type, source, ms)
        return


register_command_handler(handler_gdeya, 'гдея', ['все', 'мук'], 80, 'Показывет список конференций где сидит бот и дополнительную информацию, такую как ник бота в той конференции и количество юзеров', 'гдея', ['гдея'])