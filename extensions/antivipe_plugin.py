#===istalismanplugin===
# -*- coding: utf-8 -*-

# Endless / talisman rev 79+
# version 1.0
# Ported from AntiVipe bot by Avinar (avinar@xmpp.ru)

# licence show in another plugins ;)

# mod by 40tman

AVIPES={}
AUTO_PRO=[]
AVSERVERS=['diary.ru','livejournal.com','vk.com','gajim.org','myjabber.ru','ya.ru','jabber.perm.ru','gmail.com','jabber.ru','xmpp.ru', 'jabbers.ru', 'xmpps.ru', 'qip.ru', 'talkonaut.com', 'jabbus.org','gtalk.com','jabber.cz','jabberon.ru','jabberid.org','linuxoids.net','jabber.kiev.ua','jabber.ufanet.ru','jabber.corbina.ru']
BANSERV_LAST=[]
RED_SERVERS=[u'kaluga.org',u'alpha-labs.net',u'jabber.zp.ua',u'burtonini.com',u'braxis.org',u'pop3.ru',u'bugfactory.org',u'jabber.fr',u'jabber.454.ru',u'jabber.chirt.ru',u'aqq.eu',u'newserv.intellectronika.ru',u'jabber.openchaos.org',u'jabber.altline.ru',u'dollchan.ru',u'volity.net']


def bott_in_room(groupchat):
        if not groupchat in GROUPCHATS:
                return 0
        bn=handler_botnick(groupchat)
        if not bn in GROUPCHATS[groupchat]:
                return 0
        if not 'joined' in GROUPCHATS[groupchat][bn]:
                return 0
        if time.time()-GROUPCHATS[groupchat][bn]['joined']>60:
                return 1
        return 0

def order_unban_v(groupchat, jid):
        iq = xmpp.Iq('set')
        iq.setTo(groupchat)
        iq.setID('ban'+str(random.randrange(1000, 9999)))
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#admin')
        query.addChild('item', {'jid':jid, 'affiliation':'none'})
        iq.addChild(node=query)
        JCON.send(iq)
        
def order_ban_v(groupchat, jid):
        if jid in AVSERVERS:
                return
        iq = xmpp.Iq('set')
        iq.setTo(groupchat)
        iq.setID('ban'+str(random.randrange(1000, 9999)))
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#admin')
        ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
        ban.setTagData('reason', u'Подозрение на вайп атаку!')
        iq.addChild(node=query)
        JCON.send(iq)
                
def get_serv(serv):
        if serv.count('@'):
                serv=serv.split('@')[1]
        if serv.count('/'):
                serv=serv.split('/')[0]
        return serv		
                
def findPresenceItemV(node):
        for p in [x.getTag('item') for x in node.getTags('x',namespace='http://jabber.org/protocol/muc#user')]:
              if p != None:
                      return p
        return None


                
def avipe_prs(prs):
        ptype = prs.getType()
        if ptype == 'unavailable' and prs.getStatusCode() == '303':
                nick = prs.getNick()
                fromjid = prs.getFrom()
                groupchat = fromjid.getStripped()		
                afl=prs.getAffiliation()
                role=prs.getRole()
                avipe_join(groupchat, nick, afl, role)

def order_kick_v(groupchat, nick, reason=''):
        iq = xmpp.Iq('set')
        iq.setTo(groupchat)
        iq.setID('kick'+str(random.randrange(1000, 9999)))
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#admin')
        kick=query.addChild('item', {'nick':nick, 'role':'none'})
        kick.setTagData('reason', handler_botnick(groupchat)+': '+reason)
        iq.addChild(node=query)
        JCON.send(iq)
        
def avipe_join(groupchat, nick, afl, role):
        acc = int(user_level(groupchat+'/'+nick, groupchat))
        if acc>15:
                return
        if not bott_in_room(groupchat):
                return
        global AVIPES
        jid = handler_jid(groupchat+'/'+nick)
        if not jid:
                return
        if jid.count(u'@con'):
                return
        jid_serv = jid.split('@')[1]
        if BANSERV_LAST:
                BANSERV_LAST.pop()
        BANSERV_LAST.append(jid_serv)
        if not groupchat in AVIPES:
                return
        if jid_serv in AVSERVERS:
                return
        global INFO	
        ttime=int(time.time())	
        if time.time() - INFO['start'] < 70:	
                return
        
        if (ttime - AVIPES[groupchat]['ltime']) > 20:
                AVIPES[groupchat]['ltime']=ttime
                AVIPES[groupchat]['num']=0
                AVIPES[groupchat]['jids']=[jid]
                if groupchat in AUTO_PRO:
                        AUTO_PRO.remove(groupchat)
                        msg(groupchat,u'/me вроде тише стало,не буду пока серверы трогать.')
                return
        AVIPES[groupchat]['num']+=1
        AVIPES[groupchat]['jids'].append(jid)
        joined=AVIPES[groupchat]['jids']
        global GROUPCHATS
        if len(joined) > 3:
                if not groupchat in AUTO_PRO:
                        AUTO_PRO.append(groupchat)
                        if source[1] not in POL_SEX.keys():
                                msg(groupchat,u'/me перешла в боевой режим!')
                        else:
                                msg(groupchat,u'/me перешел в боевой режим!')
                        hnd_avipe_ban(groupchat)
                AVIPES[groupchat]['ltime']=ttime
                x=len(joined)
                if (get_serv(joined[x-2]) == get_serv(joined[x-1])) and (get_serv(joined[x-3]) == get_serv(joined[x-1])):    #and joined[x-2] != joined[x-1]:
                        serv=get_serv(joined[x-2])
                        if not serv in AVSERVERS:			
                                order_ban_v(groupchat,serv)					
                        node=''
                        for nick in GROUPCHATS[groupchat].keys():
                                if get_serv(handler_jid(groupchat+'/'+nick)) == serv and GROUPCHATS[groupchat][nick]['ishere']:
                                        order_kick_v(groupchat, nick)
                        if node:
                                order_kick_v(groupchat, nick)

                        if not serv in AVSERVERS:
                                for nick in GROUPCHATS[groupchat].keys():
                                        if user_level(groupchat+'/'+nick, groupchat) > 19:
                                                #if GROUPCHATS[groupchat][nick]['status'] in [u'online',u'chat',u'away']:
                                                msg(groupchat+'/'+nick, u'Внимание! Сервер '+serv+u' занесен в бан лист!')

        if AVIPES[groupchat]['num'] > 4:
                order_ban_v(groupchat, jid)
                

def avipe_call(type, source, parameters):
        global AVIPES
        PATH='dynamic/'+source[1]+'/antivipe.txt'
        parameters=parameters.strip().lower()
        if parameters:
                if check_file(source[1],'antivipe.txt'):
                        if parameters=='on' or parameters=='1' or parameters==u'вкл':
                                write_file(PATH, 'on')
                                AVIPES[source[1]]={'ltime':0, 'num':0, 'jids': []}
                                reply(type, source, u'Функция антивайпа включена!')
                        elif parameters=='off' or parameters=='0' or parameters==u'выкл':
                                write_file(PATH, 'off')
                                if source[1] in AVIPES:
                                        del AVIPES[source[1]]
                                reply(type, source, u'Функция антивайпа отключена!')
                        else:
                                reply(type, source, u'Читай помощь по команде!')
        else:
                if not source[1] in AVIPES:
                        reply(type, source, u'Вы отключили функцию антивайпа!')
                else:
                        reply(type, source, u'Функция антивайпа включена!')


def avipe_init(groupchat):
        if check_file(groupchat,'antivipe.txt'):
                if not read_file('dynamic/'+groupchat+'/antivipe.txt')=='off':
                        AVIPES[groupchat]={'ltime':0, 'num':0, 'jids': []}


def protect_spam_serv(groupchat,nick,afl,role):
        if groupchat in AUTO_PRO:
                jid = handler_jid(groupchat+'/'+nick)
                serv = jid.split('@')[1]
                if serv in AVSERVERS:
                        return
                try:
                        order_ban_v(groupchat, serv)
                        msg(groupchat, u'/me добавил в баню '+serv)
                except:
                        pass
                
def antivipe_ban_serv(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if parameters:
                i = parameters.lower()
                if i.count(u'ласт')>0:
                        l=''
                        for x in BANSERV_LAST:
                                l+=x+'; '
                                if x in AVSERVERS:
                                        reply(type,source,x+u' запрещено банить')
                                        return
                                order_ban_v(source[1], x)
                        reply(type,source,l+u' в бане')
                        return
                if i.count(u'вайп')>0:
                        l=''
                        for x in RED_SERVERS:
                                l+=x+','
                                order_ban_v(source[1], x)
                        reply(type,source,u'следующие сервера занесены в бан-лист:\n'+l)
                        return
                if i.count(u'урожай')>0:
                        if not source[1] in AUTO_PRO:
                                AUTO_PRO.append(source[1])
                                reply(type,source,u'принимаем урожай!')
                                return
                        else:
                                AUTO_PRO.remove(source[1])
                                reply(type,source,u'прием урожая окончен')
                                return
                order_ban_v(source[1], parameters)
                reply(type,source,parameters+u' в бане')

def hnd_avipe_ban(groupchat):
        fl='dynamic/spamserv.txt'
        if os.path.exists(fl):
                txt=eval(read_file(fl))
                for x in txt:
                        order_ban_v(groupchat, x)

def avipe_spam_add(type, source, parameters):
        if not parameters:
                reply(type, source, u'?')
                return
        if parameters.isspace() or not parameters.count('@'):
                return
        fl='dynamic/spamserv.txt'
        if os.path.exists(fl):
                txt=eval(read_file(fl))
                if parameters.lower() in txt:
                        reply(type, source, u'this server in not new, and hi use now')
                        return
                else:
                        txt.append(parameters.lower())
                        write_file(fl, str(txt))
                        reply(type, source, u'add!') 

register_command_handler(avipe_spam_add, '!спамсерв', ['мод','антивайп', 'админ'], 20, 'добавляет сервер в базу бана при вайп атаках.', '!спамсерв сервер', ['!спамсерв anythin.ru'])
register_join_handler(protect_spam_serv)              
register_presence_handler(avipe_prs)
register_join_handler(avipe_join)
register_command_handler(avipe_call, 'антивайп', ['мод','антивайп', 'админ'], 20, 'Включение/отключение функции защиты от вайп атак. Способно защитить от примитивных и средних атак. По умолчанию включен.', 'антивайп [<1/on/вкл/0/off/выкл>]', ['антивайп on','антивайп off'])
register_command_handler(antivipe_ban_serv, 'бансерв', ['мод','антивайп', 'админ'], 20, 'Банит сервер,ключ команды ласт-выводит и банит сервер последнего входящего;ключ вайп-заносит основные сервера используемые вайп-ботами в бан-лист', 'бансерв <сервер>', ['бансерв jabber.zp.ua','бансерв ласт'])
register_stage1_init(avipe_init)	

