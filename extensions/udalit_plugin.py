#===istalismanplugin===
# -*- coding: utf-8 -*-

sp_ud=[]
def handler_r_del(type,source,parameters):
        #print '1'
        if not source[1] in GROUPCHATS:
                return
        if source[2] == handler_botnick(source[1]) or source[2]=='':
                return
        if int(user_level(source[1]+'/'+source[2],source[1]))>14:
               reply(type,source,u'команда только для гостей и мемберов!')
               return
        if '1' in sp_ud:
                reply(type,source,u'попробуй чуть позже')
                return
        else:
                sp_ud.append('1')
        if source[2] in GROUPCHATS[source[1]]:
                #print '2'
                if GROUPCHATS[source[1]][source[2]]['ishere']==1:
                        n=0
                        c=0
                        #print '3'
                        while GROUPCHATS[source[1]][source[2]]['ishere']==1:
                                i=random.randrange(0, 9)
                                n+=1
                                if n<100:
                                        c=1
                                elif n>100 and n<200:
                                        c=2
                                elif n>200 and n<300:
                                        c=3
                                elif n>300 and n<400:
                                        c=4
                                elif n>400 and n<500:
                                        c=5
                                elif n>500 and n<600:
                                        c=6
                                elif n>600 and n<700:
                                        c=7
                                elif n>700 and n<800:
                                        c=8
                                elif n>800 and n<900:
                                        c=9
                                elif n>900 and n<1000:
                                        c=10
                                if c==10:
                                        sp_ud.remove('1')
                                        delete_kick(source[1],source[2],u'error 404:room no found')
                                        break
                                JCON.send(xmpp.protocol.Message(source[1]+'/'+source[2],u'удаление начато.Дождитесь конца удаления,иначе процесс будет остановлен.Всего удалено '+unicode(c)+unicode(i)+u'%','chat'))
                                

def delete_kick(groupchat, nick, reason):
        iq = xmpp.Iq('set')
        iq.setTo(groupchat)
        iq.setID('kick'+str(random.randrange(1000, 9999)))
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#admin')
        kick=query.addChild('item', {'nick':nick, 'role':'none'})
        kick.setTagData('reason', handler_botnick(groupchat)+': '+reason)
        iq.addChild(node=query)
        JCON.send(iq)                 


register_command_handler(handler_r_del, 'удалить', ['все'], 10, 'удаляет конференцию', 'удалить', ['удалить'])
