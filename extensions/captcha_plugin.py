#===istalismanplugin===
# -*- coding: utf-8 -*-

CP_NT={}
CP_AV={}
NUM_CP={}
PRIV_PR=[]

def hnd_cp_join(groupchat,nick,afl,role):
        jid=handler_jid(groupchat+'/'+nick)
        serv=jid.split('@')[1]
        if time.time() - INFO['start'] < 60:	
                return
        try:
                if jid.count('@conference.'):
                        return
                if groupchat in NUM_CP:
                        if time.time() - NUM_CP[groupchat]['time']>NUM_CP[groupchat]['off']:
                                captcha_bot_con(groupchat,'0','0')
                                del NUM_CP[groupchat]
        except:
                print('timer captcha error')
        if not groupchat in CP_AV:
                return
        if (serv==u'jabber.ru') | (serv==u'qip.ru'):
                return
        if (time.time() - CP_AV[groupchat]['ltime'])>20 and len(nick)<21:
                CP_AV[groupchat]['ltime']=time.time()
                CP_AV[groupchat]['num']=0
                CP_AV[groupchat]['jids']=[jid]
                return
        CP_AV[groupchat]['num']+=1
        CP_AV[groupchat]['jids'].append(jid)
        joined=CP_AV[groupchat]['jids']
        if len(joined) > 2:
                CP_AV[groupchat]['ltime']=time.time()
        rt=str(random.randrange(180, 360))
        if CP_AV[groupchat]['num'] == 4:
                if groupchat in NUM_CP:
                        return
                captcha_bot_con(groupchat,'1','0')
                NUM_CP[groupchat]={'time':time.time(),'off':rt}


def set_cfg_captcha(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if not parameters:
                return
        if check_file(source[1],'captcha.txt'):
                        file='dynamic/'+source[1]+'/captcha.txt'
                        fp=open(file,'r')
                        txt=eval(fp.read())
                        fp.close()
        if source[2]==handler_botnick(source[1]):
                return
        if parameters=='1':
                txt['TO']=1
                write_file(file,str(txt))
                reply(type,source,u'members only установлено')
                return
        if parameters=='0':
                txt['TO']=0
                write_file(file,str(txt))
                reply(type,source,u'captcha установлено')
                return
        l=parameters.lower()
        if l.count(u';')<2:
                reply(type,source,u'попробуй ввести логин;сервер;пароль')
                return
        s=parameters.split(u';')
        if len(s[0].strip())>2:
                txt['LOGIN']=s[0].strip()
                write_file(file,str(txt))
        if len(s[1].strip())>5:
                txt['SERVER']=s[1].strip()
                write_file(file,str(txt))
        if len(s[2].strip())>2:
                txt['PASS']=s[2].strip()
                write_file(file,str(txt))
        reply(type,source,u'конфиг успешно настроен!')


def hnd_captcha_work(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if not parameters:
                reply(type,source,u'1-чтоб включить,0-отключить')
                return
        n='2'
        if parameters=='1':
                n='1'
        if parameters=='0':
                n='0'
        if n=='2':
                return
        reply(type,source,u'ok')
        captcha_bot_con(source[1],n,'0')

def captcha_bot_con(groupchat,n,private):
        new_jid=0
        if check_file(groupchat,u'captcha.txt'):
                file='dynamic/'+groupchat+u'/captcha.txt'
                fp=open(file,'r')
                txt=eval(fp.read())
                fp.close()
        else:
                return
        if 'SERVER' in txt:
                SERVER=txt['SERVER']
        else:
                SERVER=''
        if 'LOGIN' in txt:
                LOGIN=txt['LOGIN']
        else:
                LOGIN=''
        if 'PASS' in txt:
                PASS=txt['PASS']
        else:
                PASS=''
        if 'TO' in txt:
                TO=txt['TO']
        else:
                TO='0'
        if (SERVER=='') | (LOGIN=='') | (PASS==''):
                new_jid=1
                SERVER='jabber.ru'
                LOGIN=str(random.randrange(110000, 999999))
                PASS=str(random.randrange(100000, 999999))+str(time.time())
        var="captcha_protected"
        if TO==1:
                var="muc#roomconfig_membersonly"
        if private=='1':
                var="allow_private_messages"
                n='0'
        if private=='2':
                var="allow_private_messages"
                n='1'
        node,domain,resource,password=LOGIN,SERVER,u'QIP',PASS
        jid = xmpp.JID(node=node, domain=domain, resource=resource)
        cl = xmpp.Client(jid.getDomain(), debug=[])
        con = cl.connect()
        if not con:
                msg(groupchat,u'error connect '+unicode(SERVER))
                return
        if new_jid:
                xmpp.features.register(cl, domain, {'username': node, 'password':password})
        au=cl.auth(jid.getNode(), password, jid.getResource())
        if not au:
                msg(groupchat,u'ошибка аутентификации')
                return
        cl.sendInitPresence()
        if new_jid:
                txt['SERVER']=SERVER
                txt['LOGIN']=LOGIN
                txt['PASS']=PASS
                write_file(file, str(txt))
                msg(groupchat,u'ваш jid овнер-бота '+LOGIN+'@'+SERVER)
        threading.Thread(None, cap_join, 'at'+str(random.randrange(0, 999)), (cl,groupchat,n,var)).start()

def cap_join(cl,groupchat,n,var):
        if not groupchat in CP_NT:
                CP_NT[groupchat]={}
        nick = u'Antivipe'+str(random.randrange(199, 999))
        mess = xmpp.protocol.Presence(groupchat+'/'+nick)
        mess.setTag('x', namespace=xmpp.NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
        try:
                cl.send(mess)
        except:
                pass
        time.sleep(2)
        iq = xmpp.Iq('set')
        iq.setTo(groupchat)
        query = xmpp.Node('query')
        query.setNamespace('http://jabber.org/protocol/muc#owner')
        x = xmpp.Node('x',{'type':'submit'})
        x.setNamespace(xmpp.NS_DATA)
        inv=x.addChild('field', {'var':"FORM_TYPE"})
        inv.setTagData('value', xmpp.NS_MUC_ROOMCONFIG)
        cap=x.addChild('field', {'var':var})
        cap.setTagData('value', n)
        query.addChild(node=x)
        iq.addChild(node=query)
        cl.send(iq)
        time.sleep(3)
        try:
                cl.disconnect()
        except:
                pass

def avcap_call(type, source, parameters):
        global CP_AV
        PATH='dynamic/'+source[1]+'/capwork.txt'
        parameters=parameters.strip().lower()
        if parameters:
                if check_file(source[1],'capwork.txt'):
                        if parameters=='on' or parameters=='1' or parameters==u'вкл':
                                write_file(PATH, 'on')
                                CP_AV[source[1]]={'ltime':0, 'num':0, 'jids': []}
                                reply(type, source, u'Функция автокапча включена!')
                        elif parameters=='off' or parameters=='0' or parameters==u'выкл':
                                write_file(PATH, 'off')
                                if source[1] in CP_AV:
                                        del CP_AV[source[1]]
                                reply(type, source, u'Функция автокапча отключена!')
                        else:
                                reply(type, source, u'Читай помощь по команде!')
        else:
                if not source[1] in CP_AV:
                        reply(type, source, u'Вы отключили функцию автокапчи!')
                else:
                        reply(type, source, u'Функция автокапча включена!')


def cap_init(groupchat):
        if check_file(groupchat,u'capwork.txt'):
                if not read_file('dynamic/'+groupchat+'/capwork.txt')=='off':
                        CP_AV[groupchat]={'ltime':0, 'num':0, 'jids': []}

def show_cap_jid(type,source,parameters):
        if not source[1] in GROUPCHATS:
                return
        if check_file(source[1],'captcha.txt'):
                fp=open('dynamic/'+source[1]+'/captcha.txt')
                txt=eval(fp.read())
                fp.close()
                if 'LOGIN' in txt and 'SERVER' in txt:
                        if txt['LOGIN']:
                                reply(type,source,txt['LOGIN']+'@'+txt['SERVER'])
                                return
                        else:
                                reply(type,source,'no found')

def cap_priv_protect(raw,type,source,parameters):
        if source[1] in GROUPCHATS and type=='private':
                if not source[1] in CP_AV:
                        return
                acc=int(user_level(source[1]+'/'+source[2], source[2]))
                if acc>10:
                        return
                if acc<0:
                        return
                if source[2] in GROUPCHATS[source[1]]:
                        if 'joined' in GROUPCHATS[source[1]][source[2]]:
                                if time.time()-GROUPCHATS[source[1]][source[2]]['joined']<3:
                                        if not source[1] in PRIV_PR:
                                                msg(source[1],u'временно отключаю приват в связи с подозрением на вайп!')
                                                PRIV_PR.append(source[1])
                                                captcha_bot_con(source[1],'0','1')
                                                time.sleep(600)
                                                PRIV_PR.remove(source[1])
                                                captcha_bot_con(source[1],'1','2')
                                                return
                        s=parameters
                        if parameters.count(' '):
                                s=parameters.split()[0]
                        if not s.lower() in COMMANDS and len(parameters)>500:
                                if not source[1] in PRIV_PR:
                                        msg(source[1],u'временно отключаю приват в связи с подозрением на вайп!')
                                        PRIV_PR.append(source[1])
                                        captcha_bot_con(source[1],'0','1')
                                        time.sleep(600)
                                        PRIV_PR.remove(source[1])
                                        captcha_bot_con(source[1],'1','2')
                                        return
                        if 'idle' in GROUPCHATS[source[1]][source[2]]:
                                if time.time()-GROUPCHATS[source[1]][source[2]]['idle']<3:
                                        if not source[1] in PRIV_PR:
                                                msg(source[1],u'временно отключаю приват в связи с подозрением на вайп!')
                                                PRIV_PR.append(source[1])
                                                captcha_bot_con(source[1],'0','1')
                                                time.sleep(600)
                                                PRIV_PR.remove(source[1])
                                                captcha_bot_con(source[1],'1','2')
                                                return
                                
register_message_handler(cap_priv_protect)                             
register_join_handler(hnd_cp_join)
register_command_handler(show_cap_jid, 'капча_жид', ['мод','админ','антивайп'], 20, 'Показывает жид овнер-бота', 'капча_жид', ['капча_жид'])
register_command_handler(avcap_call, 'капча_ав', ['мод','админ','антивайп'], 20, 'Включает автокапчу при вайп атаках', 'капча_ав <0|1>', ['капча_ав 1'])
register_command_handler(hnd_captcha_work, 'капча', ['мод','антивайп'], 30, 'Наладочная тест-команда.При настроенном овнер-боте включает/отключает капчу.Для этого должен быть настроен <капча_конфиг>,-в команде указываеться учетка с правами овнера', 'капча <0|1>', ['капча 1'])
register_command_handler(set_cfg_captcha, 'капча_конфиг', ['мод','антивайп'], 30, 'Настройка аккаунта овнер-бота и включение капчи <капча_конфиг 0> либо включение membersonly - <капча_конфиг 1>.По умолчанию стоит вкл.капчи.Для смены данных аккаунта овнер-бота просто введите их заново,старые при этом удаляться.Указывайте учетку у которой есть права овнера в комнате.', 'капча_конфиг логин;сервер;пароль', ['капча_конфиг 40tman;jabber.perm.ru;12345'])
register_stage1_init(cap_init)
