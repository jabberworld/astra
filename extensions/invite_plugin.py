#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  invite_plugin.py


invite_pending=[]
INVITE_LIM={}

def hnd_inv_user(type, source, parameters):
        sp='0'
        handler_invite_start(type, source, parameters, sp)

def handler_invite_start(type, source, parameters, sp):
        truejid,nick,reason='','',''
        if not parameters:
                reply(type,source,u'ииии?')
                return
        LIST=[u'овнеров',u'админов',u'мемберов',u'всех']
        if parameters.lower() in LIST:
                if not source[1] in INVITE_LIM:
                        INVITE_LIM[source[1]]={'time':time.time()}
                else:
                        if time.time() - INVITE_LIM[source[1]]['time']<60:
                                reply(type,source,u'слишком быстро')
                                return
                        else:
                                INVITE_LIM[source[1]]['time']=time.time()
                reply(type,source,u'Приглашение выслано')
                get_invite_jid(type,source,parameters)
                return
        if not parameters.count('@'):
                nicks = GROUPCHATS[source[1]].keys()
                nick=parameters.split()[0]
                if not nick in nicks:
                        reply(type,source,u'юзер не наден, попробуйте ввести jid')
                        return
                else:
                        truejid=handler_jid(source[1]+'/'+nick)
                        reason=' '.join(parameters.split()[1:])
        else:
                truejid=parameters
        msg=xmpp.Message(to=source[1])
        id = 'inv'+str(random.randrange(1, 1000))
        globals()['invite_pending'].append(id)
        msg.setID(id)
        x=xmpp.Node('x')
        x.setNamespace('http://jabber.org/protocol/muc#user')
        inv=x.addChild('invite', {'to':truejid})
        if reason:
                inv.setTagData('reason', reason)
        else:
                inv.setTagData('reason', u'Вас приглашает '+source[2])
        msg.addChild(node=x)
#	print unicode(msg)
#	JCON.SendAndCallForResponse(msg, handler_invite_answ,{'type': type, 'source': source})
        JCON.send(msg)
        if sp!='1':
                reply(type,source,u'призвала')

def get_invite_jid(type,source,par):
        LIST={u'овнеров':u'owner',u'админов':u'admin',u'мемберов':u'member'}
        if par.lower() in LIST:
                hnd_getinv_start(type,source,LIST[par.lower()])
                return
        else:
                if par.lower()==u'всех':
                        for x in LIST:
                                hnd_getinv_start(type,source,LIST[x])


def hnd_getinv_start(type,source,par):
        iq = xmpp.Iq('get')
        id='item'+str(random.randrange(1000, 9999))
        iq.setTo(source[1])
        iq.setID(id)
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#admin')
        ban=query.addChild('item', {'affiliation':par})
        iq.addChild(node=query)
        JCON.SendAndCallForResponse(iq, hnd_getinv_ans, {'type': type,'source': source, 'par': par})

def hnd_getinv_ans(coze, res, type, source, par):
        id=res.getID()
        rep =''
        allinf=''
        n=0
        al=0
        if res:
                if res.getType() == 'result':
                        at=res.getFrom()
                        mas=res.getQueryChildren()
                        for x in mas:
                                try:
                                        jid=x.getAttrs()['jid']
                                        if jid.count('@'):
                                                handler_invite_start(type, source, jid, '1')
                                except:
                                        pass
                                     
                                        
register_command_handler(hnd_inv_user, '!призвать', ['мук','все'], 10, 'Может приглашать заданного пользователя в конференцию,либо пользователей со списка owner, admin, member', 'призвать [ник/JID] [причина]', ['призвать админов','призвать мемберов','призвать всех','призвать guy','призвать guy@jabber.aq','призвать guy@jabber.aq есть дело'])
