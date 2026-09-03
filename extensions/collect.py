# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
        
BLACK_LIST = 'dynamic/blacklist.txt'

CHAT_CACHE = {}
AMSGBL = []
CHAT_DIRTY = {}

def handler_chat_cache(stanza, ltype, source, body):
        try:
                subject = stanza.getTag('subject')
        except:
                subject = False
        if ltype != 'public' or subject or not source[2]:
                return
        header = u'[%s] %s» ' % (time.strftime('%H:%M:%S (%d.%m.%Y) GMT', time.gmtime()), source[2])
        CHAT_CACHE[source[1]]['1'] = CHAT_CACHE[source[1]]['2']
        if len(body) > 256:
                body = body[:256]+'[...]'
        CHAT_CACHE[source[1]]['2'] = header+body

def _clean_send(conf, count, text = u''):
        zero = xmpp.Message(conf, text, mtype = "groupchat")
        zero.setTag("body")
        for i in range(1, count + 1):
                try: JCON.send(zero)
                except IOError: return
                INFA['outmsg'] += 1
                if i < count:
                        time.sleep(1.4)

def _clean_count(body, conf):
        window = CONF_HISTORY.get(conf, 0)
        count = window if window > 20 else 24
        for token in (body or u'').split():
                if check_number(token):
                        number = int(token)
                        if 0 < number <= 100:
                                count = number
                        break
        return count

def handler_clean(mType, source, body):
        if source[1] not in GROUPCHATS:
                return
        first = (body or u'').split()
        if first and first[0].lower() == u'размер':
                window = CONF_HISTORY.get(source[1], 0)
                used = window if window > 20 else 24
                reply(mType, source, u'Размер окна для текущей конфы: %d (история при входе: %d). По умолчанию чищу %d сообщений.' % (used, window, used))
                return
        count = _clean_count(body, source[1])
        mode = None
        for token in (body or u'').split():
                low = token.lower()
                if low in (u'тихо', u'беспалева', u'видно'):
                        mode = low
                        break
        if mode == u'тихо':
                if mType != "private":
                        change_bot_status(source[1], u"Чистка...", "dnd")
                _clean_send(source[1], count)
                if mType != "private":
                        message = STATUS[source[1]]["message"]
                        status = STATUS[source[1]]["status"]
                        change_bot_status(source[1], message, status)
        elif mode == u'беспалева':
                _clean_send(source[1], count)
        elif mode == u'видно':
                _clean_send(source[1], count, u"•")
        else:
                mis = [u'Зачистка начата :) ',u'Антиупарыватель конфы запущен!',u'4.....3.....2.....1.....ПОЕХАЛИ!!!',u'Мыло душистое! Пена пушистая! Изыдти нафиг мессаги! Во имя Конфы и всех Участников. Фтопку!',u'Убью того, кто так на гадил!!!',u'Э... Нанимай уборщицу',u'Ну смотря сколько платишь',u'И чито я буду с этого иметь?',u'Купи себе скатерть самобранку']
                mis2 = [u'ога, гатова :) ',u'антиупарывание прошло успешно 8) ',u'Все убрано, можно и отдохнуть *BEACH* ',u'Полет нормальный',u'Ничтяк *DANCE* ',u'В следующий раз юзай моющий пылесос',u'5 баксов с тебя',u'Может тебе еще и лизгинка сплясать?!']
                mes = random.choice(mis)
                kl = random.choice(mis2)
                if mType != "private":
                        reply(mType, source, mes)
                _clean_send(source[1], count)
                if mType != "private":
                        reply(mType, source, kl)

def last_chat_cache(type, source, body):
        confs = sorted(GROUPCHATS.keys())
        if body:
                body = body.lower()
                if body in confs:
                        conf = body
                elif check_number(body):
                        number = int(body) - 1
                        if number >= 0 and number <= len(confs):
                                conf = confs[number]
                        else:
                                conf = False
                else:
                        conf = False
                if conf:
                        cache = ''
                        if CHAT_CACHE[conf]['1']:
                                cache += '\n'+CHAT_CACHE[conf]['1']
                        if CHAT_CACHE[conf]['2']:
                                cache += '\n'+CHAT_CACHE[conf]['2']
                        if not cache:
                                cache = u'пусто'
                        reply(type, source, cache)
                else:
                        reply(type, source, u'меня там нет!')
        else:
                col, list = 0, ''
                for conf in confs:
                        col = col + 1
                        list += u'\n№ '+str(col)+'. - '+conf
                reply(type, source, list)

def handler_test(type, source, body):
        if time.localtime()[1]==4 and time.localtime()[2]==1:
                testfr = [u"КОТЭ ОПАСНОСТЕ!!11", u"ТЕЛОИД11111", 
                                u"ГОЛАКТЕГО ОПАСНОСТЕ1111", u"ПЫЫщщщщщЩЩЬ!!111", u"АДИНАДИН!!!!"
                                u"ЪЖСЛО111", u"ЧАКЕ НЕГОДУЕ......", u"ОНОТОЛЕ СЕРЧАЕ.", u"КОТЭ РАДУЕ!1", u"ПИПЛ ШОкЕ11"]
        else:
                testfr = [u'Что?', u'Провален, твой IQ = 90!', u'Пассед', u'Нормачка =^_^=', u'- Тест на дебила выключен, ты опоздал', u'Две полоски О_о', u'Сейчас, сейчас! Протестим твою репу на удароустойчивость!',u'Ломай меня полностью! :-D',u'Я хочу чтобы ты ломал меня.... :-[ ',u'пиши "хелп" чтобы.....  :-O :-[ Ой бля... >пассед< :-D']
                
        reply(type, source, (random.choice(testfr))+(' (Bot PID: %s)' % str(BOT_PID)))

def handler_admin_message(type, source, body):
        if body:
                args = body.split()
                if len(args) >= 2:
                        jid = args[0].strip()
                        if jid.count('@') and jid.count('.'):
                                inst = jid.split('/')[0].lower()
                                if jid.count('@conf') and inst not in GROUPCHATS:
                                        reply(type, source, u'меня нет в этой конфе')
                                else:
                                        mess = body[(body.find(' ') + 1):].strip()
                                        if len(mess) <= 1024:
                                                msg(jid, u'Сообщение от '+source[2]+': '+mess)
                                                reply(type, source, u'сделано')
                                        else:
                                                reply(type, source, u'Слишком длинная мессага!')
                        else:
                                reply(type, source, u'Ээ нет, это вообще не жид!')
                else:
                        reply(type, source, u'А что слать-то?')
        else:
                reply(type, source, u'ты чё-то тупишь')

def handler_admin_say(type, source, body):
        if body:
                if len(body) <= 256:
                        msg(source[1], body)
                else:
                        msg(source[1], body[:256])
        else:
                reply(type, source, u'Ну а дальше?')

def handler_global_message(type, source, body):
        if body:
                for conf in GROUPCHATS.keys():
                        msg(conf, u'### Сообщение от '+source[2]+':\n'+body)
                reply(type, source, u'Мессага успешно разослана')
        else:
                reply(type, source, u'А что слать то?')

def handler_auto_message(type, source, body):
        if body:
                jid = handler_jid(source[0])
                if jid in AMSGBL:
                        reply(type, source, u'тебе запрещено отсылать мессаги админу')
                elif len(body) <= 1024:
                        delivery(u'Сообщение от '+source[2]+' ('+jid+'): '+body)
                        reply(type, source, u'сделано')
                else:
                        reply(type, source, u'Слишком длинная мессага!')
        else:
                reply(type, source, u'Ну а дальше?')

def handler_amsg_blacklist(type, source, body):
        if body:
                args = body.split()
                if len(args) == 2:
                        jid = args[1].strip()
                        if jid.count('@') and jid.count('.'):
                                check = args[0].strip()
                                if check == '+':
                                        if jid not in AMSGBL:
                                                AMSGBL.append(jid)
                                                write_file(BLACK_LIST, str(AMSGBL))
                                                repl = u'добавлен %s в чёрный список' % (jid)
                                        else:
                                                repl = u'этот жид и так там'
                                elif check == '-':
                                        if jid in AMSGBL:
                                                AMSGBL.remove(jid)
                                                write_file(BLACK_LIST, str(AMSGBL))
                                                repl = u'удален %s из чёрного списка' % (jid)
                                        else:
                                                repl = u'этого жида и так там нет'
                                else:
                                        repl = u'инвалид синтакс'
                        else:
                                repl = u'ан нет, это вообще не жид!'
                else:
                        repl = u'инвалид синтакс'
        else:
                repl, col = u'Чёрный список:', 0
                for jid in AMSGBL:
                        col = col + 1
                        repl += '\n'+str(col)+'. '+jid
                if col == 0:
                        repl = u'Чёрный список пуст'
        reply(type, source, repl)

def amsg_blacklist_init():
        if initialize_file(BLACK_LIST, '[]'):
                globals()['AMSGBL'] = load_file(BLACK_LIST, [])
        else:
                Print('\n\nError: can`t create black list file!', color2)

def chat_cache_init(conf):
        CHAT_CACHE[conf] = {'1': '', '2': ''}
        CHAT_DIRTY[conf] = True

## ---- XEP-0313 MAM + XEP-0425 модерация (команда "чисть_мам") ----

MAM_COLLECT = {}   # queryid -> dict(conf, nick, limit, count, done)
MAM_RESULTS = {}   # queryid -> [(stanza_id, nick_from), ...]
LAST_MAM_TRIGGER_SID = {}   # conf -> stanza_id последней команды чисть_мам
MAM_SEQ = [0]
MAM_USE_LEGACY = False  # True -> apply-to/fasten:0 (старый ejabberd)
MAM_RSM_BEFORE = True  # True -> <max>N</max> + <before/> (последняя страница); False -> только <max>N</max>
MAM_DEBUG_FILE = 'dynamic/mam_debug.txt'

def _mam_log(msg):
        try:
                line = u'[%s] %s\n' % (time.strftime('%H:%M:%S (%d.%m.%Y) GMT', time.gmtime()), msg)
                write_file(MAM_DEBUG_FILE, line, 'a')
        except Exception:
                try:
                        Print('mam_debug write error')
                except Exception:
                        pass

def _mam_reset_debug():
        try:
                write_file(MAM_DEBUG_FILE, u'')
        except Exception:
                pass

def _safe_xml(stanza):
        try:
                xml = stanza.toXml()
                if not isinstance(xml, str):
                        xml = str(xml)
                return xml.replace('\n', ' ')
        except Exception:
                return u'<no-xml>'

def _mam_next_id():
        MAM_SEQ[0] += 1
        return str(MAM_SEQ[0])

def _mam_send_moderate(conf, stanza_id):
        iq = xmpp.Iq(to = conf, typ = 'set', id = 'mam-mod-%s' % _mam_next_id())
        if MAM_USE_LEGACY:
                apply_to = iq.addChild('apply-to', attrs = {'id': stanza_id}, namespace = xmpp.NS_FASTEN)
                moderate = apply_to.addChild('moderate', namespace = xmpp.NS_MODERATE_0)
        else:
                moderate = iq.addChild('moderate', attrs = {'id': stanza_id}, namespace = xmpp.NS_MODERATE)
        moderate.addChild('retract', namespace = xmpp.NS_RETRACT if not MAM_USE_LEGACY else xmpp.NS_RETRACT_0)
        moderate.setTagData('reason', u'Moderated via чисть_мам')
        INFA['outiq'] += 1
        JCON.send(iq)

def _mam_fin_answer(coze, stanza, qid):
        data = MAM_COLLECT.get(qid, None)
        _mam_log(u'=== FIN qid=%s data_present=%s stanza_none=%s type=%s ==='
                 % (qid, data is not None, stanza is None, (getattr(stanza, 'getType', lambda: None)() if stanza else u'')))
        if stanza is not None:
                _mam_log(u'FIN xml: %s' % _safe_xml(stanza))
        _mam_log(u'FIN results_before_wait: %d' % len(MAM_RESULTS.get(qid, [])))
        time.sleep(1.0)
        _mam_log(u'FIN results_after_wait: %d' % len(MAM_RESULTS.get(qid, [])))
        if not data:
                return
        results = MAM_RESULTS.pop(qid, [])
        conf = data['conf']
        nick = data['nick']
        limit = data['limit']
        if nick:
                results = [(sid, rnick) for (sid, rnick) in results if rnick == nick]
        results = results[-limit:]
        _mam_log(u'FIN filtered: got=%d nick=%s limit=%d' % (len(results), nick, limit))
        for (sid, rnick) in results:
                _mam_log(u'FIN moderate sid=%s nick=%s' % (sid, rnick))
                _mam_send_moderate(conf, sid)
                time.sleep(0.15)
        reply(data['mType'], data['source'], u'Удалено из MAM: %d сообщений.' % (len(results)))
        if stanza is None and not results and data.get('source'):
                reply(data['mType'], data['source'], u'Не удалось получить историю (таймаут).')

def _mam_start(conf, nick, limit, mType, source, exclude_sid = u''):
        qid = 'mam-c-%s' % _mam_next_id()
        # Собираем с запасом, чтобы после исключения собственных сообщений бота
        # и самой команды-триггера всё равно осталось >= limit записей для удаления.
        # Окно делаем заметно больше limit, т.к. новейшие сообщения забиты
        # «церемонией чистки» (акки бота + команды).
        fetch_max = max(limit * 3, limit + 20)
        MAM_COLLECT[qid] = {'conf': conf, 'nick': nick, 'limit': limit,
                            'mType': mType, 'source': source,
                            'exclude_sid': exclude_sid}
        MAM_RESULTS[qid] = []
        iq = xmpp.Iq(to = conf, typ = 'set', id = qid)
        query = iq.addChild('query', attrs = {'queryid': qid}, namespace = xmpp.NS_MAM)
        x = query.addChild('x', attrs = {'type': 'submit'}, namespace = xmpp.NS_DATA)
        field = x.addChild('field', attrs = {'var': 'FORM_TYPE', 'type': 'hidden'})
        field.addChild('value', payload = xmpp.NS_MAM)
        rsm = query.addChild('set', namespace = xmpp.NS_RSM)
        rsm.addChild('max', payload = str(fetch_max))
        if MAM_RSM_BEFORE:
                rsm.addChild('before')
        INFA['outiq'] += 1
        _mam_reset_debug()
        try:
                JCON._raw_log_open_window(6.0)
        except Exception:
                pass
        _mam_log(u'=== SEND === qid=%s conf=%s nick=%s limit=%s type=%s' % (qid, conf, nick, limit, mType))
        _mam_log(u'IQ: %s' % _safe_xml(iq))
        JCON.SendAndCallForResponse(iq, _mam_fin_answer, {'qid': qid})

def handler_mam_result(stanza, fromjid, instance):
        result = stanza.getTag('result')
        if result is None or result.getNamespace() != xmpp.NS_MAM:
                return
        qid = result.getAttr('queryid')
        _mam_log(u'MSG arrives: qid=%s from=%s type=%s instance=%s' % (qid, fromjid, stanza.getType(), instance))
        _mam_log(u'MSG xml: %s' % _safe_xml(stanza))
        if not qid or qid not in MAM_COLLECT:
                _mam_log(u'MSG SKIP (qid not in MAM_COLLECT): qid=%s known=%s' % (qid, qid in MAM_COLLECT))
                return
        forwarded = result.getTag('forwarded')
        message = forwarded.getTag('message') if forwarded else None
        if message is None:
                _mam_log(u'MSG NO message element (forwarded=%s)' % (forwarded is not None))
                return
        nick = u''
        frm = message.getAttr('from')
        if frm and '/' in frm:
                nick = frm.rsplit('/', 1)[1]
        sid = u''
        conf = MAM_COLLECT[qid]['conf']
        for stanza_id in message.getTags('stanza-id'):
                if (stanza_id.getNamespace() == xmpp.NS_SID and
                    (stanza_id.getAttr('by') or '').lower() == conf.lower()):
                        sid = stanza_id.getAttr('id') or u''
                        break
        _mam_log(u'MSG HANDLED qid=%s sids_found=%d sid=%s nick=%s conf=%s'
                 % (qid, len(message.getTags('stanza-id')), sid, nick, conf))
        if sid:
                # Никогда не удаляем собственные сообщения бота.
                if nick == handler_botnick(conf):
                        _mam_log(u'MSG SKIP (bot self): nick=%s' % nick)
                        return
                # Не удаляем само сообщение-команду, которым вызвана чистка.
                if sid == MAM_COLLECT[qid].get('exclude_sid'):
                        _mam_log(u'MSG SKIP (trigger command): sid=%s' % sid)
                        return
                MAM_RESULTS[qid].append((sid, nick))

def handler_clean_mam(mType, source, body):
        if source[1] not in GROUPCHATS:
                return
        args = (body or u'').split()
        nick = None
        limit = 1
        if args:
                if not check_number(args[0]):
                        nick = args[0]
                        if len(args) > 1:
                                if check_number(args[1]):
                                        limit = int(args[1])
                else:
                        limit = int(args[0])
        if limit < 1:
                limit = 1
        if limit > 100:
                limit = 100
        reply(mType, source, u'Удаляю через MAM: %d сообщений%s...' % (limit, (u' (ник: %s)' % nick) if nick else u''))
        _mam_start(source[1], nick, limit, mType, source, LAST_MAM_TRIGGER_SID.get(source[1], u''))

register_message_handler(handler_chat_cache)
register_mam_handler(handler_mam_result)
command_handler(handler_clean, 15, "collect")
command_handler(handler_clean_mam, 15, "collect")
command_handler(last_chat_cache, 20, "collect")
command_handler(handler_test, 10, "collect")
command_handler(handler_admin_message, 100, "collect")
command_handler(handler_admin_say, 20, "collect")
command_handler(handler_global_message, 100, "collect")
command_handler(handler_auto_message, 10, "collect")
command_handler(handler_amsg_blacklist, 100, "collect")
register_stage0_init(amsg_blacklist_init)

register_stage1_init(chat_cache_init)
