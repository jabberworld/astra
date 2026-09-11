#===istalismanplugin===
# /* coding: utf-8 */
# (c) simpleApps Unofficial, 2011
# Distributed under Apache 2.0 license
# See www.apache.org/licenses/LICENSE-2.0 for more details.

# *** configuration ***

__configuration = {"jid": "astra61292@jabber.ru",
                                                  "password": "lenivec",
                                                  "port": 5222}

__status = "same status"

__resource = "Psi+"
# end configuration

__chats = {}

__clients = {}

__run = False

def dispatcher(cl):
        while __run:
                cl.Process(15) 

def clone_me(mType, toJID, args):
        globals()["__run"] = True
        for x in __configuration.keys():
                globals()[x] = __configuration[x]
        username, server = jid.split("@")
        __client = xmpp.Client(server, port, [])
        connect = __client.connect(server = (server, port), secure = 0,
                                               use_srv = True)
        if connect:
                reply(mType, toJID, u"%s. Подключение удалось. Авторизация..." % str(__client))
        else:
                reply(mType, toJID, u"Подключение не удалось.")
                return
        auth = __client.auth(username, password, "%s[%d]" % (__resource, len(__clients.keys())))
        if not auth:
                reply(mType, toJID, "Auth error: %s/%s." % (repr(__client.lastErr), repr(__client.lastErrCode)))
                return
        __clients[args.strip()] = __client
        threading.Thread(target = dispatcher, args = (__client,)).start()
        return True

def clone_presence(pType, room, nick):
        if pType == "join":
                __chats[room] = str()
                prs = xmpp.protocol.Presence(room+"/"+nick)
                prs.setStatus(__status)
                prs.setShow('chat')
                pres = prs.setTag('x', namespace = xmpp.NS_MUC)
                pres.addChild('history', {'maxchars':'0'})
                __clients[nick.strip()].send(prs)
        else:
                if room in __chats: del __chats[room]
                prs = xmpp.Presence(room, "unavailable")
                prs.setStatus("remote server not-found")
                for x in __clients:
                        __clients[x].send(prs)

def handleCMD(mType, toJID, args):
        if args.split()[0] in ("kill", u"выкл"):
                for x in __chats.keys():
                        clone_presence("unv", x, "")
                globals()["__run"] = False
                globals()["__chats"] = {}
                globals()["__clients"] = {}
                return
        if args in __clients:
                reply(mType, toJID, u"\"%s\" уже запущен." % repr(args))
                clone_presence("join", toJID[1], args)
                return	
        if clone_me(mType, toJID, args):
                clone_presence("join", toJID[1], args)

register_command_handler(handleCMD, 'клон', ['все'], 100, 'Создаёт клон-бота [ник/kill/выкл]\n(c) simpleApps Unofficial, 2011.', 'клон <ник>|<действие>', ['клон слон', 'клон выкл'])