#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Milka bot
#  idle_plugin.py

#  Initial © 2013 Gigabyte & ShtrihKot (C) Stalker Team


idle_pending=[]


def handler_idle(type, source, parameters):
        idle_iq = xmpp.Iq('get')
        id='idle'+str(random.randrange(1000, 9999))
        globals()['idle_pending'].append(id)
        idle_iq.setID(id)
        idle_iq.addChild('query', {}, [], 'jabber:iq:last');
        
        if parameters:
                param = parameters.strip()
                idle_iq.setTo(param)
        else:
                param=CONNECT_SERVER
                idle_iq.setTo(param)
                
        JCON.SendAndCallForResponse(idle_iq, handler_idle_answ, {'type': type, 'source': source, 'param': param})
        
                
def handler_idle_answ(coze, res, type, source, param):
        if res is None:
                reply(type, source, u'таймаут')
                return
        id=res.getID()
        
        if id in globals()['idle_pending']:
                globals()['idle_pending'].remove(id)
        else:
                print('ooops!  (idle_plugin)')
                return
                
        rep =''
        
        if res:
                if res.getType()=='error':
                        reply(type,source,u'там или нету жабер сервера или он упал или он запрещает смотреть эту инфу')
                        return
                        
                elif res.getType() == 'result':
                        sec = ''
                        props = res.getPayload()
                        
                        if not props:
                                reply(type,source,u'там или упал жабер сервер или его вообще нету')
                                return 
                                
                        for p in props:
                                sec=p.getAttrs()['seconds']
                                
                                if sec.count(',') == 1:
                                        sec = sec.replace(',', '.')
                                        
                                if not sec == '0':
                                        try:
                                                rep = param+u' работает уже '+timeElapsed(float(sec))
                                        except:
                                                rep = param+u' не ясный ответ от сервера'
        else:
                rep = u'глюк'
                
        reply(type, source, rep)

new_idle_pending=[]


def handler_new_idle(type, source, parameters):
        nick=parameters
        groupchat=source[1]
        
        if nick == source[2] or not parameters:
                reply(type, source, u'И чё я тебе должна написать? *SCRATCH*')
                return
                
        iq = xmpp.Iq('get')
        id = 'p'+str(random.randrange(1, 1000))
        globals()['new_idle_pending'].append(id)
        iq.setID(id)
        iq.addChild('query', {}, [], 'jabber:iq:last');
        
        if parameters:
                if nick not in GROUPCHATS[source[1]] or not GROUPCHATS[source[1]][nick]['ishere']==1:
                        reply(type, source, u'Не вижу таких здесь *PARDON*')
                        return
                        
                if source[1] in GROUPCHATS:
                        nicks = GROUPCHATS[source[1]].keys()
                        param = parameters.strip()
                        
                        if not nick in nicks:
                                iq.setTo(param)
                        else:
                                if GROUPCHATS[groupchat][nick]['ishere']==0:
                                        reply(type, source, u'а он тут? :-O')
                                        return
                                        
                                param=nick
                                jid=groupchat+'/'+nick
                                iq.setTo(jid)
                                
        t0 = time.time()
        JCON.SendAndCallForResponse(iq, handler_new_idle_answ,{'t0': t0, 'mtype': type, 'source': source, 'param': param})
        return

        
def handler_new_idle_answ(coze, res, t0, mtype, source, param):
        if source[1] in GROUPCHATS:
                nick = param.strip()
                
                if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']==1:
                        groupchat = source[1]
                        idletime = int(time.time() - GROUPCHATS[groupchat][nick]['idle'])
                        id = res.getID()
                        
                        if id in globals()['new_idle_pending']:
                                globals()['new_idle_pending'].remove(id)
                        else:
                                print('someone is doing wrong... (idle_plugin)')
                                return
                                
                        if res:
                                if res.getType() == 'result':
                                        if param:
                                                try:
                                                        res = str(res)
                                                        res = res.split('<query seconds="')[1].split('"')[0]
                                                        globaltime = int(res)
                                                        otvet = u'\nпо стэнзe: '+timeElapsed(globaltime)+u' назад.'
                                                except:
                                                        otvet = u''
                                else:
                                        otvet = u''
                                        
                        reply(mtype, source, nick+u' заснул(а) в комнате: '+timeElapsed(idletime)+u' назад.'+otvet)
        

register_command_handler(handler_idle, 'аптайм', ['все','никто'], 10, 'Показывает аптайм определённого сервера.', 'аптайм <сервер>', ['аптайм jabber.aq'])
register_command_handler(handler_new_idle, 'жив', ['все','никто'], 10, 'Показывает сколько времени неактивен юзер.\nАвтор: GavYur\nИдея: ShtrihKot', 'жив <ник>', ['жив guy'])
