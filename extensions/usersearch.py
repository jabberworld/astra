#===istalismanplugin===
# -*- coding: utf-8 -*-

USER_SEARCH = {'search':0, 'chat':[], 'user':[], 'con':0, 'error':False}

BASE_CONFS = [u'conference.jabber.ru', u'conference.talkonaut.com', u'conference.qip.ru', u'conference.jabbrik.ru']

def _disco_items(target, cb):
        iq = xmpp.Iq(to = target, typ = 'get')
        iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
        try:
                JCON.SendAndCallForResponse(iq, cb, {})
        except:
                USER_SEARCH['error'] = True

def _on_rooms(coze, stanza):
        if not stanza or stanza.getType() != 'result':
                USER_SEARCH['error'] = True
                return
        try:
                props = stanza.getQueryChildren()
        except:
                props = None
        if not props:
                return
        for x in props:
                try:
                        att = x.getAttrs()
                except:
                        continue
                j = att.get('jid')
                if j:
                        USER_SEARCH['chat'].append(j)

def _on_users(coze, stanza):
        if not stanza or stanza.getType() != 'result':
                return
        try:
                props = stanza.getQueryChildren()
        except:
                props = None
        if not props:
                return
        for x in props:
                try:
                        att = x.getAttrs()
                except:
                        continue
                j = att.get('jid')
                if j:
                        USER_SEARCH['user'].append(j)
                else:
                        nm = att.get('name')
                        if nm:
                                USER_SEARCH['user'].append(nm)

def hnd_usersearch(type, source, parameters):
        global USER_SEARCH
        if USER_SEARCH['search']:
                reply(type, source, u'Сейчас выполняется поиск! Попробуйте через пару минут!')
                return
        if not parameters:
                reply(type, source, u'А кого искать будем?')
                return
        parameters = parameters.strip().lower()
        USER_SEARCH['search'] = 1
        USER_SEARCH['chat'] = []
        USER_SEARCH['user'] = []
        USER_SEARCH['error'] = False
        reply(type, source, u'Результат смотри в привате через ~3 минуты!')
        try:
                _run_search(source, parameters)
        except:
                USER_SEARCH['error'] = True
                lytic_crashlog(hnd_usersearch)
        finally:
                USER_SEARCH['search'] = 0
                USER_SEARCH['chat'] = []
                USER_SEARCH['user'] = []
                USER_SEARCH['con'] = 0

def _run_search(source, parameters):
        for host in BASE_CONFS:
                _disco_items(host, _on_rooms)
        deadline = time.time() + 20
        while time.time() < deadline:
                if USER_SEARCH['error'] or len(USER_SEARCH['chat']) >= 1:
                        break
                time.sleep(0.5)
        time.sleep(3)
        rooms = sorted(set(USER_SEARCH['chat']))
        for room in rooms:
                _disco_items(room, _on_users)
        deadline = time.time() + 35
        while time.time() < deadline:
                time.sleep(0.5)
        total_nicks = len(set(USER_SEARCH['user']))
        if total_nicks == 0:
                reply('private', source, u'Совпадений не найдено!\nВсего конференций: '+str(len(BASE_CONFS))+u'\nВсего ников проверено: 0')
                return
        found = {}
        for u in USER_SEARCH['user']:
                room = u.split('/')[0] if '/' in u else u
                nick = u.split('/')[1] if '/' in u else u
                if parameters in nick.lower():
                        found.setdefault((room, nick), None)
        if not found:
                reply('private', source, u'Совпадений не найдено!\nВсего конференций: '+str(len(BASE_CONFS))+u'\nВсего ников проверено: '+str(total_nicks))
                return
        lines = []
        for (room, nick) in sorted(found):
                lines.append(room+' '+nick)
        text = u'Результатов '+str(len(lines))+u':\n'+'\n'.join(lines)[:2000]+u'\nВсего конференций: '+str(len(BASE_CONFS))+u'\nВсего ников проверено: '+str(total_nicks)
        reply('private', source, text)

register_command_handler(hnd_usersearch, '!отыскать', ['все'], 0, 'отыскать', 'отыскать', ['отыскать'])

register_command_handler(hnd_usersearch, 'отыскать', ['все','поиск','юзеры'], 0, 'Поиск юзера онлайн по нику в лучших чатах сети jabber.\nАвтоматически не чувствителен к капсу (A - a), различию русских и английских символов в нике (Y - У) и нестрогому соотвествию параметров к нику ( вас = Вася, Василий и т.п) ', 'отыскать <ник>', ['отыскать вася'])
