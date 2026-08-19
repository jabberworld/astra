# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  mucacc_plugin.py

# CallForResponse (c) Gigabyte
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

BanBase = {}
BanBaseFile = "dynamic/banbase.txt"

def IQSender(mType, source, conf, item_name, item, afrls, afrl, nick, rsn = None):
        stanza = xmpp.Iq(to = conf, typ = 'set')
        INFA['outiq'] += 1
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_MUC_ADMIN)
        afl_role = query.addChild('item', {item_name: item, afrls: afrl})
        if rsn:
                afl_role.setTagData('reason', rsn)
        stanza.addChild(node = query)
        JCON.SendAndCallForResponse(stanza, handler_afrls_answer, {'mType': mType, 'source': source})

def IQSender111(mType, source, conf, item_name, item, afrls, afrl, nick, rsn = None):
        stanza = xmpp.Iq(to = conf, typ = 'set')
        INFA['outiq'] += 1
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_MUC_ADMIN)
        afl_role = query.addChild('item', {item_name: item, afrls: afrl})
        if rsn:
                afl_role.setTagData('reason', rsn)
        stanza.addChild(node = query)
        JCON.SendAndCallForResponse(stanza, handler_afrls_answer111, {'mType': mType, 'source': source})

def IQSender_member(mType, source, conf, item_name, item, afrls, afrl, nick, rsn = None):
        stanza = xmpp.Iq(to = conf, typ = 'set')
        INFA['outiq'] += 1
        query = xmpp.Node('query')
        query.setNamespace(xmpp.NS_MUC_ADMIN)
        afl_role = query.addChild('item', {item_name: item, afrls: afrl})
        if rsn:
                afl_role.setTagData('reason', rsn)
        stanza.addChild(node = query)
        JCON.SendAndCallForResponse(stanza, handler_afrls_answer111, {'mType': mType, 'source': source})


def handler_afrls_answer111(coze, stanza, mType, source):
        if stanza.getType() == 'result':
                reply(mType, source, "")
        else:
                reply(mType, source, u"Запрещено. Тип: %s." % stanza.getType())

def handler_afrls_answer_member(coze, stanza, mType, source):
        if stanza.getType() == 'result':
                msg(source[1], u"/me Притащила именные тапочки для %s, теперь ты постоянный участник нашего чата!") % nick
        else:
                reply(mType, source, u"Запрещено. Тип: %s." % stanza.getType())


def handler_afrls_answer(coze, stanza, mType, source):
        if stanza.getType() == 'result':
                reply(mType, source, u"Сделано.")
        else:
                reply(mType, source, u"Запрещено. Тип: %s." % stanza.getType())

def handler_ban2(mType, source, conf, jid, nick, reason):
        IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'outcast', nick, reason)
def handler_none2(mType, source, conf, jid, nick, reason):
        IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'none', nick, reason)
def handler_member2(mType, source, conf, jid, nick, reason):
        IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'member', nick, reason)
def handler_member3(mType, source, conf, jid, nick, reason):
        IQSender_member(mType, source, conf, 'jid', jid, 'affiliation', 'member', nick, reason)
def handler_admin2(mType, source, conf, jid, nick, reason):
        IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'admin', nick, reason)
def handler_owner2(mType, source, conf, jid, nick, reason):
        IQSender(mType, source, conf, 'jid', jid, 'affiliation', 'owner', nick, reason)
def handler_kick2(mType, source, conf, nick, reason):
        IQSender(mType, source, conf, 'nick', nick, 'role', 'none', nick, reason)
def handler_visitor2(mType, source, conf, nick, reason):
        IQSender(mType, source, conf, 'nick', nick, 'role', 'visitor', nick, reason)
def handler_participant2(mType, source, conf, nick, reason):
        IQSender(mType, source, conf, 'nick', nick, 'role', 'participant', nick, reason)
def handler_moder2(mType, source, conf, nick, reason):
        IQSender(mType, source, conf, 'nick', nick, 'role', 'moderator', nick, reason)

COLKICK = {}
COLBAN = {}

def command_kick(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        jid = handler_jid('%s/%s' % (source[1], nick))
                        if jid not in ADLIST:
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_kick2(mType, source, source[1], nick, reason)
                        else:
                                reply(mType, source, u'кикать своего админа? да ни за что!')
                else:
                        reply(mType, source, u'кого?')
        else:
                reply(mType, source, u'приколист :-D')

def save_colkick():
        global COLKICK
        fp = file('dynamic/colcick.txt', 'w')
        fp.write( str(COLKICK) )
        fp.close()

def save_colban():
        global COLBAN
        fp = file('dynamic/colban.txt', 'w')
        fp.write( str(COLBAN) )
        fp.close()

def command_visitor(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        jid = handler_jid('%s/%s' % (source[1], nick))
                        if jid not in ADLIST:
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_visitor2(mType, source, source[1], nick, reason)
                        else:
                                reply(mType, source, u'затыкать своего админа? да ни за что!')
                else:
                        reply(mType, source, u'кого?')
        else:
                reply(mType, source, u'приколист :-D')

def command_participant(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        if len(args) >= 2:
                                reason = body[(body.find(' ') + 1):].strip()
                        else:
                                reason = source[2]
                        handler_participant2(mType, source, source[1], args[0].strip(), reason)
                else:
                        reply(mType, source, u'кого?')
        else:
                reply(mType, source, u'приколист :-D')

def command_moder(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        if len(args) >= 2:
                                reason = body[(body.find(' ') + 1):].strip()
                        else:
                                reason = source[2]
                        handler_moder2(mType, source, source[1], args[0].strip(), reason)
                else:
                        reply(mType, source, u'кого выделывать то?')
        else:
                reply(mType, source, u'приколист :-D')

def command_member(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_member2(mType, source, source[1], jid, nick, reason)
                        else:
                                reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
                else:
                        reply(mType, source, u'кого выделывать то?')
        else:
                reply(mType, source, u'приколист :-D')

def command_admin(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_admin2(mType, source, source[1], jid, nick, reason)
                        else:
                                reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
                else:
                        reply(mType, source, u'кого выделывать то?')
        else:
                reply(mType, source, u'приколист :-D')

def command_owner(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_owner2(mType, source, source[1], jid, nick, reason)
                        else:
                                reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
                else:
                        reply(mType, source, u'кого выделывать то?')
        else:
                reply(mType, source, u'приколист :-D')


def command_ban(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if jid not in ADLIST:
                                        if len(args) >= 2:
                                                reason = body[(body.find(' ') + 1):].strip()
                                        else:
                                                reason = source[2]
                                        handler_ban2(mType, source, source[1], jid, nick, reason)
                                else:
                                        reply(mType, source, u'своего админа? да ни за что!')
                        else:
                                reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
                else:
                        reply(mType, source, u'кого?')
        else:
                reply(mType, source, u'приколист :-D')

def command_none(mType, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if len(args) >= 2:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                handler_none2(mType, source, source[1], jid, nick, reason)
                        else:
                                reply(mType, source, u'Хрень пишешь! Это не жид и юзеров с таким ником здесь небыло!')
                else:
                        reply(mType, source, u'кого?')
        else:
                reply(mType, source, u'приколист :-D')

def command_fullban(mType, source, body):
                if body:
                        args = body.split()
                        nick = args[0].strip()
                        if nick.count('.') or nick in GROUPCHATS[source[1]]:
                                if nick in GROUPCHATS[source[1]]:
                                        jid = handler_jid('%s/%s' % (source[1], nick))
                                else:
                                        jid = nick
                                if len(args) > 1:
                                        reason = body[(body.find(' ') + 1):].strip()
                                else:
                                        reason = source[2]
                                if BanBase.get(jid):
                                        reply(mType, source, u"Этот пользователь уже глобально забанен.")
                                        return
                                else:
                                        BanBase[jid] = {"date": time.strftime("%d.%m.%Y (%H:%M:%S)"),
                                                                     "reason": reason}
                                        write_file(BanBaseFile, str(BanBase))
                                for conf in GROUPCHATS.keys():
                                        handler_banjid(conf, jid, reason)
                                answer = u"Сделано."
                        else:
                                answer = u"Это не JID и юзеров с таким ником здесь не было."
                elif BanBase:
                        answer = str()
                        num = 0
                        for jid in BanBase.keys():
                                date, reason = BanBase[jid].values()
                                num += 1
                                answer +=  u"\n%i. %s (%s) [%s]." % (num, jid, reason, date)
                else:
                        answer = u"В базе фуллбана пусто."
                reply(mType, source, answer)

def command_fullunban(mType, source, jid):
        if jid:
                if jid.count('.') and not jid.count(' '):
                        if jid in BanBase:
                                del BanBase[jid]
                                write_file(BanBaseFile, str(BanBase))
                        for conf in GROUPCHATS.keys():
                                handler_unban(conf, jid)
                        reply(mType, source, u'Сделано.')
                else:
                        reply(mType, source, u'Хрень пишешь! Это не жид!')
        else:
                reply(mType, source, u'кого разбанивать то?')

def banbase_init():
        if initialize_file(BanBaseFile, "{}"):
                globals()["BanBase"] = load_file(BanBaseFile, {})
        else:
                Print('\n\nError: can`t create banbase.txt!', color2)


def handler_unban1(conf, jid):
        handler_iq_send(conf, 'jid', jid, 'affiliation', 'member')


def AdminBan(conf, nick, reason, code):
        if code:
                if code == '301':
                        jid = handler_jid(conf+'/'+nick)
                        if jid in ADLIST:
                                msg(conf,u'Админа нельзя банить!!! авторазбан для "'+nick+u'"')
                                time.sleep(3)
                                handler_unban1(conf, jid)
                                return
                        elif jid in PRIVILEG.keys():
                                 if conf not in DEPRIVILEG.keys():
                                          msg(conf, u'Привилегия от админа бота! Авторазбан для '+nick)
                                          time.sleep(3)
                                          handler_unban1(conf, jid)
                                 else:
                                          return
                        else:
                                 if jid not in COLBAN.keys():
                                  COLBAN[jid] = 1
                                  save_colban()
                                 else:
                                  COLBAN[jid] += 1
                                  save_colban()
                if code == '307':
                         jid = handler_jid(conf+'/'+nick)
                         if jid not in COLKICK.keys():
                                COLKICK[jid] = 1
                                save_colkick()
                         else:
                                COLKICK[jid] += 1
                                save_colkick()

                                
register_leave_handler(AdminBan)

def privileg_prs(Prs):
   Ptype = Prs.getType()
   if Ptype != 'error':
      afl = Prs.getAffiliation()
      fromjid = Prs.getFrom()
      conf = fromjid.getStripped()
      nick = fromjid.getResource()
      jid = handler_jid('%s/%s' % (conf, nick))
      if afl == 'none':
         if jid in PRIVILEG.keys():
            if conf not in DEPRIVILEG.keys():
               handler_member(conf, nick, u'Привилегия Админа бота')
            else:
               return
         else:
            return
      else:
         return
   else:
      return

register_presence_handler(privileg_prs)

def load_colkick(*list):
        global COLKICK
        try:
                fp = file('dynamic/kolkick.txt', 'r')
                COLKICK = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/colkick.txt', 'w')
                COLKICK = {}
                fp.write( str(COLKICK) )
                fp.close()


def load_colban(*list):
        global COLBAN
        try:
                fp = file('dynamic/colban.txt', 'r')
                COLBAN = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/colban.txt', 'w')
                COLBAN = {}
                fp.write( str(COLBAN) )
                fp.close()

DEPRIVILEG = {}
PRIVILEG = {}

def hnd_privileg_add(t,s,p):
   p = p.split()[0]
   if p not in PRIVILEG.keys():
      PRIVILEG[p] = 1
      save_privileg()
      reply(t,s,u'ok')
      return
   else:
      reply(t,s,u'JID: '+p+u' уже и так с привилегией!')

register_command_handler(hnd_privileg_add, 'привилегия+', [], 100, '', '', [''])

def hnd_privileg_dell(t,s,p):
   p = p.split()[0]
   if p not in PRIVILEG.keys():
      reply(t,s,u'Не установлено для '+p)
      return
   else:
      del PRIVILEG[p]
      save_privileg()
      reply(t,s,u'ok')
      return

register_command_handler(hnd_privileg_dell, 'привилегия-', [], 100, '', '', [''])

def hnd_privileg(t,s,p):
   reply(t,s,u'Список жидов с привилегиями:\n'+str.join('\n• ', PRIVILEG))

register_command_handler(hnd_privileg, 'привилегия', [], 100, '', '', [''])

def hnd_deprivileg_add(t,s,p):
   p = p.split()[0]
   if p not in DEPRIVILEG.keys():
      DEPRIVILEG[p] = 1
      save_deprivileg()
      reply(t,s,'ok')
      return
   else:
      reply(t,s,u'CONF: '+p+u' уже и так в списке исключений для привилегий!')

register_command_handler(hnd_deprivileg_add, '!исключение+', [], 100, '', '', [''])

def hnd_deprivileg_del(t,s,p):
   p = p.split()[0]
   if p not in DEPRIVILEG.keys():
      reply(t,s,u'Адреса чата '+p+u' и так нет в списке исключений!')
      return
   else:
      del DEPRIVILEG[p]
      save_deprivileg()
      reply(t,s,u'ok')

register_command_handler(hnd_deprivileg_del, '!исключение-', [], 100, '', '', [''])

def hnd_deprivileg(t,s,p):
   reply(t,s,u'Список чатов:\n'+str.join('\n• ', DEPRIVILEG))

register_command_handler(hnd_deprivileg, '!исключения', [], 100, '', '', [''])

def load_privileg(*list):
        global PRIVILEG
        try:
                fp = file('dynamic/privileg.txt', 'r')
                PRIVILEG = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/privileg.txt', 'w')
                PRIVILEG = {}
                fp.write( str(PRIVILEG) )
                fp.close()

def save_privileg():
        global PRIVILEG
        fp = file('dynamic/privileg.txt', 'w')
        fp.write( str(PRIVILEG) )
        fp.close()

def load_deprivileg(*list):
        global DEPRIVILEG
        try:
                fp = file('dynamic/deprivileg.txt', 'r')
                DEPRIVILEG = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/deprivileg.txt', 'w')
                DEPRIVILEG = {}
                fp.write( str(DEPRIVILEG) )
                fp.close()

def save_deprivileg():
        global DEPRIVILEG
        fp = file('dynamic/deprivileg.txt', 'w')
        fp.write( str(DEPRIVILEG) )
        fp.close()

register_stage1_init(load_deprivileg)
register_stage1_init(load_privileg)
register_stage1_init(load_colkick)
register_stage1_init(load_colban)
register_stage0_init(banbase_init)
command_handler(command_moder, 20, "mucacc")
command_handler(command_member, 20, "mucacc")
register_command_handler(command_member, 'тапки', [], 15, 'дать участнику мембера', 'тапки ник', ['тапки Кот'])
command_handler(command_admin, 30, "mucacc")
command_handler(command_owner, 30, "mucacc")
command_handler(command_kick, 15, "mucacc")
command_handler(command_visitor, 15, "mucacc")
register_command_handler(command_visitor, 'девойс', [], 15, 'забрать голос', 'девойс ник', ['девойс Кот'])
command_handler(command_participant, 15, "mucacc")
register_command_handler(command_participant, 'войс', [], 15, 'дать голос', 'войс ник', ['войс Кот'])
command_handler(command_none, 20, "mucacc")
command_handler(command_ban, 20, "mucacc")
command_handler(command_fullban, 80, "mucacc")
command_handler(command_fullunban, 80, "mucacc")
