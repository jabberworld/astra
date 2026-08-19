# BS mark.1-55
# /* coding: utf-8 */

def udisco_answer_1(some, stanza, mType, source, body, limit):
        if xmpp.isResultNode(stanza):
                for node in stanza.getQueryChildren():
                        name = node.getAttr("name")
                        n_users = name.split(' ')[-1]
                        if n_users[1:-1].isdigit():
                                if int(n_users[1:-1]) > 0:
                                        iq = xmpp.Iq("get", to = node.getAttr("jid"))
                                        iq.addChild("query", namespace = xmpp.NS_DISCO_ITEMS)
                                        desc = {"mType": mType, "source": source, "body": body, "limit": 16}
                                        JCON.SendAndCallForResponse(iq, udisco_answer_2, desc)

def udisco_answer_2(some, stanza, mType, source, body, limit):
        if xmpp.isResultNode(stanza):
                for node in stanza.getQueryChildren():
                        if body == node.getAttr("name"):
                                reply(mType, source, 'найден в: %s' % node.getAttr("jid").split('/')[0])

def command_usearch(mType, source, body):
        if body:
                        if mType != 'private' or mType != 'chat':
                                reply(mType, source, 'Начинаю поиск пользователя %s.. результат появится в привате' % body)
                        else:
                                reply(mType, source, 'Начинаю поиск пользователя %s..' % body)
                        iq = xmpp.Iq("get", to = "conference.jabber.ru")
                        iq.addChild("query", namespace = xmpp.NS_DISCO_ITEMS)
                        desc = {"mType": 'private', "source": source, "body": body, "limit": 16}
                        JCON.SendAndCallForResponse(iq, udisco_answer_1, desc)
        else:
                reply(mType, source, 'Кого ищем?')

command_handler(command_usearch, 10, "usearch")
