# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1

#  Author: SaranskCity

def handler_puk(type, source, nick):
        if type == 'public':
                if nick:
                        if not nick == handler_botnick(source[1]):
                                if nick in GROUPCHATS[source[1]]:
                                        reply(type, source, u'%s пукнул со звуком в %s децибел' % (nick, random.randint(10, 160)))
                                else:
                                        reply(type, source, u'такого пердуна тут нет!')
                        else:
                                reply(type, source, u'я не пукаю я же бот!')
                else:
                        reply(type, source, u'Ты пукнул со звуком в %s децибел' % random.randint(10, 160))
        else:
                reply(type, source, u'Ты пукнул со звуком в %s децибел' % random.randint(10, 160))

command_handler(handler_puk, 10, "puk")
