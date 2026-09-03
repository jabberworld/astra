# SPEC.md — Полная техническая спецификация проекта «Astra»

> Исчерпывающая спецификация, позволяющая по описанию воссоздать аналогичный проект.
> Astra — Jabber/XMPP-бот для MUC-конференций. Форк BlackSmith mark.1 на Python 3 + slixmpp 1.17
> через слой совместимости с legacy-API `xmpppy`.
>
> Автор кода: BlackSmith (команды «Witcher» / «simpleApps»), переработка под Python 3.

---

## Оглавление

1. [Назначение и функциональность](#1-назначение-и-функциональность)
2. [Требования к среде и зависимостям](#2-требования-к-среде-и-зависимостям)
3. [Конфигурация](#3-конфигурация)
4. [Структура проекта](#4-структура-проекта)
5. [Запуск и жизненный цикл](#5-запуск-и-жизненный-цикл)
6. [Слой XMPP (`xmpp.py`)](#6-слой-xmpp-xmpppy)
7. [Ядро `astra.py`](#7-ядро-astrapy)
8. [Обработка станз](#8-обработка-станз)
9. [Namespace'ы и XEP'ы](#9-namespaceы-и-xepы)
10. [Глобальные реестры и словари](#10-глобальные-реестры-и-словари)
11. [Система прав и доступов](#11-система-прав-и-доступов)
12. [Плагинная система](#12-плагинная-система)
13. [Макросистема](#13-макросистема)
14. [Справочная система (help)](#14-справочная-система-help)
15. [Персистентность данных](#15-персистентность-данных)
16. [Сетевые и утилитные модули](#16-сетевые-и-утилитные-модули)
17. [MUC-жизненный цикл и роли](#17-muc-жизненный-цикл-и-роли)
18. [MAM/Архив (XEP-0313) и модерация (XEP-0425)](#18-mam-архив-xep-0313-и-модерация-xep-0425)
19. [Ошибки, краши, перезапуск](#19-ошибки-краши-перезапуск)
20. [Тесты и диагностика](#20-тесты-и-диагностика)
21. [Полный каталог плагинов](#21-полный-каталог-плагинов)
22. [Полный каталог справочных команд](#22-полный-каталог-справочных-команд)

---

## 1. Назначение и функциональность

Astra — многофункциональный администратор Jabber-конференций (MUC) и развлекательный бот:
- подключение к XMPP-серверу (TLS), авторизация, вступление в набор комнат;
- слежение за присутствием: вход/выход, кик/бан, смена ника, смена ролей/аффилиации;
- обработка текстовых команд и push-сообщений;
- управление правами и ролями участников (модератор/админ/овире);
- защита: антибот, антиспам, антивайп, антиспэйс, flood-контроль, ростер-верификация;
- игры и развлечения (викторина, миллионер, 21 очко, снежки, морской бой, рулетка, дуэль...);
- утилиты: погода, перевод, поиск, городы/расстояние, DNS, vCard и т.д.;

Ядро реализует весь протокол, плагины — конкретное поведение. Плагины исполняются
`execfile`'ом в глобальное пространство `astra` и имеют прямой доступ ко всем функциям и данным ядра.

---

## 2. Требования к среде и зависимостям

- **Python 3** (проект портирован с Python 2; алиасы `basestring`/`unichr`/`unicode`/`file` в `astra.py`).
- **slixmpp == 1.17.0** (асинхронная XMPP-библиотека).
- **requests** (для `webtools`).
- sqlite3 (стандартная библиотека, используется `itypes.Database`).
- ОС на базе Unix (используются `os.uname()`, `ps -o rss`, `os.execl`).

Запуск: `python3 astra.py`.

---

## 3. Конфигурация

Файл `config.py` (локальный, в `.gitignore`). Шаблон — `config.example.py`.

| Ключ | Описание |
|---|---|
| `SERVER` | XMPP-домен/JID-домен |
| `CONNECT_SERVER` | сервер для TCP-подключения |
| `PORT` | TCP-порт (5222 или 5223) |
| `HOST` | значение host |
| `SECURE` | `True` — TLS-подключение |
| `USERNAME` | локальная часть JID |
| `PASSWORD` | пароль |
| `RESOURCE` | ресурс (часть полного JID) |
| `DEFAULT_NICK` | ник бота в комнате по умолчанию (`u'Astra'`) |
| `CHAT_MSG_LIMIT` | макс. длина исходящего сообщения в общий чат (4048) |
| `PRIV_MSG_LIMIT` | макс. длина исходящего в приват (8960) |
| `INC_MSG_LIMIT` | макс. длина входящего сообщения, обрезается (8960) |
| `MSERVE` | режим охраны: работать без прав админа или нет |
| `BOSS` | JID суперадмина (уровень 100) |
| `MEMORY_LIMIT` | лимит памяти RSS (КБ), 0 — выкл. (самоубийство при превышении) |
| `GLOBACCESS_FILE` | путь к файлу глобальных доступов |
| `GROUPCHATS_FILE` | путь к списку комнат |
| `QUESTIONS_FILE` | база вопросов для ростер-верификации |
| `ROSTER_FILE` | файл состояния ростера/верификации |
| `PLUGIN_DIR` | каталог плагинов |
| `PID_FILE` | файл PID |
| `NETWORK_PROXY` | прокси для сетевых запросов (может быть `socks5h://...`) |
| `NETWORK_TIMEOUT` | таймаут сетевых запросов (сек) |
| `WEATHER_RESPONSE_FILE` | файл кэша погоды |

---

## 4. Структура проекта

```
astra/
├── astra.py            # ядро, событийный цикл, обработчики, загрузка плагинов, main()
├── xmpp.py             # слой совместимости xmpppy <-> slixmpp, namespace'ы, Client
├── config.py / config.example.py
├── enconf.py           # chkFile/nameEncode — кодирование имён конференций на диск
├── itypes.py           # Number, Database(sqlite3)
├── sTools.py           # getArchitecture()
├── simplejson.py       # shim -> stdlib json
├── webtools.py         # read_url, uHTML, stripTags, IDNA, byteFormat ...
├── pattern.py          # Pattern/JIDPattern/NickPattern (шаблоны с *)
├── macros.py           # макро/алиасы
├── fixpass.py          # пи-скрипт-фиксатор py2->py3
├── PID.txt
├── extensions/         # 209 плагинов .py
├── help/               # справочники команд (python-dict), ~140 файлов
├── static/             # immutable: versions.py, вопросники, тексты, темы логов
├── dynamic/            # живые данные: базы .txt, логи, макро, каталоги комнат
├── faillog/            # crash-файлы #NN
├── logs/               # логи конференций (плагин logger)
├── tests/              # mam_diag.py, test-load.py
└── __pycache__/
```

---

## 5. Запуск и жизненный цикл

### `main()`
```
1. PID-контроль: читает PID.txt (dict {PID, START, REST[]});
   если есть старый PID и он жив — убивает; пишет новый PID.txt.
2. starting_actions():
     load_access_levels()  -> GLOBACCESS из файла
     form_admins_list()    -> ADLIST (уровень >= 80)
     load_roster_config()  -> RSTR из файла
     load_quests()         -> QUESTIONS из файла
     load_plugins()        -> загрузка плагинов
3. Connect() -> xmpp.Client, коннект, auth, RegisterHandler(message/presence/iq).
4. call_stage_init(0).
5. join_chats() -> для каждой комнаты join_groupchat() (stage1 init, presence).
6. поток proces_igra().
7. call_stage_init(2).
8. Бесконечный цикл: Dispatch_handler(calc_Timeout()).
```

### `Connect()`
```python
globals()['JCON'] = xmpp.Client(HOST, PORT, None)
JCON.connect((SERVER, PORT), None, None, False)  # или без TLS при SECURE=False
JCON.auth(USERNAME, PASSWORD, RESOURCE)
JCON.sendInitPresence()
JCON.RegisterHandler("message", MESSAGE_PROCESSING)
JCON.RegisterHandler("presence", PRESENCE_PROCESSING)
JCON.RegisterHandler("iq", IQ_PROCESSING)
```

### `calc_Timeout()`
- комнат <= 16 → 8.0 с
- комнат >= 48 → 0.2 с
- иначе → `7.8 / (Chats - 16)`

### `sys_exit(reason)`
шлёт `unavailable`, при работе > 30с вызывает stage3, затем `Exit` → рестарт через
`os.execl(sys.executable, sys.executable, astra.py)` (при «0») либо выход (при «1»).

---

## 6. Слой XMPP (xmpp.py)

Эмулирует legacy-API модуля `xmpppy`. Все методы/классы доступны через `import xmpp`.

### 6.1 Исключения
`NodeProcessed` (глотнуть станзу), `Conflict`, `SystemShutdown`, `StreamError`,
`HostUnknown`.

### 6.2 `Node` (xml-обёртка над `xml.etree.ElementTree`)
Основные методы: `getName/getNamespace/setNamespace`, `getAttr/setAttr/getAttrs`,
`getTag/getTags/getTagAttr/getTagData/getTagTag`, `setTag/setTagData/addChild`,
`getChildren/getPayload/getQueryChildren/getQueryPayload/setQueryPayload/getQueryNS`,
`getData/setData`, `buildReply(typ)`, `toXml()`, `__str__`.

Спец-accessors станзы: `getType/setType`, `getTo/setTo`, `getFrom/setFrom`,
`getID/setID`, `getTimestamp` (delay xep-0091/0203), `getErrorCode`,
`getBody/setBody`, `getSubject`, `getThread`, `getStatus/setStatus`,
`getShow/setShow`, `getPriority/setPriority`, `getReason`.

MUC-специфичные (парсит `<x xmlns='...#user'><item .../>`):
`getRole/getAffiliation/getJid/getNick/getStatusCode/getReporter`.

### 6.3 `Message` / `Presence` / `Iq`
Подклассы `Node` с конструкторами `(to, body, mtype)`, `(to, ptype, show, status)`,
`(typ, to, id)`.

### 6.4 `JID`
Парсинг `node@domain/resource`. Методы: `getNode/getDomain/getResource/getStripped`,
`bare` (property), `full` (property), `__str__`, сравнение/хэш по строке.

### 6.5 `Client`
```python
client = xmpp.Client(HOST, PORT, None)
client.connect((SERVER, PORT), None, None, use_srv)
client.auth(USERNAME, PASSWORD, RESOURCE)   # -> "sasl" | False
client.RegisterHandler("message"|"presence"|"iq", fn)
client.sendInitPresence()
client.send(stanza_or_xml_str)
client.Process(timeout)          # просто time.sleep (ядро гоняет само)
client.isConnected() / isTls()
client.Roster.*                  # getItems/Authorize/Subscribe/Unsubscribe/setItem/delItem
client.SendAndCallForResponse(stanza, func, args, timeout=30)
client._raw_log_open_window(sec) / _raw_log(...)
```

**Отладка сырых станз**: методы `_raw_log_open_window(seconds)` и `_raw_log(data)`
пишут в `dynamic/raw_log.txt`; окно открывается на N секунд после вызова.

### 6.6 Внутренняя диспетчеризация (`_connect_real`)

Создаётся `slixmpp.ClientXMPP(full_jid, password)` в потоке с собственным `asyncio`-loop:
- `verify_certificates = False`;
- регистрируются плагины `xep_0077`, `xep_0199`;
- события: `"message"`→`_on_message`, `"presence"`→`_on_presence`,
  `"disconnected"`→`_on_disconnected`, `"tls_success"`→`_on_tls_success`;
- низкоуровневые колбэки (`Callback`):
  - `legacy_iq` (`MatchXPath("{jabber:client}iq")`) → `_on_iq`;
  - `legacy_message` (`MatchXPath("{jabber:client}message")`) → `_on_message_low`.

**Ключевая особенность для MAM**: станзы `<message><result xmlns='urn:xmpp:mam:2'>`
**не** порождают событие slixmpp `message`, поэтому их ловит `legacy_message`
через `_on_message_low` и отдаёт в диспетчер `message`-хендлеров ядра.

Каждый драйвер `_on_*` → `self._dispatch(self._handlers[ns], Message/Presence/Iq(real=ev))`;
`_dispatch` вызывает все зарегистрированные handlers, проглатывая `NodeProcessed`.

### 6.7 `SendAndCallForResponse`
Регистрирует временный `Callback` по `MatcherId(id)`. Если ответ приходит — вызывает
`func(client, stanza, **args)`. Если нет за `timeout` — вызывает `func(client, None, **args)`.

---

## 7. Ядро (astra.py)

### 7.1 Статистика
```python
INFO = {'start':0,'msg':0,'prs':0,'iq':0,'cmd':0,'thr':0,'errs':0}
INFA = {'outmsg':0,'outiq':0,'fr':0,'fw':0,'fcr':0,'cfw':0}
RSTR = {'AUTH':[], 'BAN':[], 'VN':'off'}   # VN: off/iq/on
LAST = {'time':0, 'cmd':'start'}
STOP = {'mto':0, 'jids':{}}
```

### 7.2 Совместимость py2
```python
basestring = str
unichr = chr
file = open
def unicode(obj, encoding=None, errors='strict')...
```

### 7.3 Утилиты
- `Print(text, color)` — цветной stdout.
- `Exit(text, exit, slp)`, `try_sleep(slp)`.
- `execfile(filename, gl)` — обёртка `exec(compile(...))`.
- `PASS_GENERATOR(codename, Number)`.
- `check_number(number)` → `int` или `False`.
- `replace_all(retxt, list, data=False)`.
- `formatWord(Numb, ls)` — склонение слов (для `timeElapsed`).
- `timeElapsed(seconds)` — формат «X дней Y часов Z минут ...».
- `that_day()` — `%Y%m%d` по Гринвичу.
- `memory_usage()` — RSS через `ps -o rss -p PID`.
- `handler_jid(full_jid)` — приводит `conf/nick` к bare JID участника или же к bare JID.
- `resolve_nick(conf, body)`, `present_nicks(conf)` — работа с никами.
- `handler_botnick(conf)` → `BOT_NICKS.get(conf, DEFAULT_NICK)`.

### 7.4 Управление файлами
- `chkFile` из `enconf` — привести имя к файловому пути.
- `initialize_file(name, data="{}")` — создать пустой/с данными файл с папками (0o755), вернуть bool.
- `read_file(name)` / `write_file(name, data, mode="w")` / `load_file(name, default)` (eval).
- `check_file(conf, file, data)` — файл в `dynamic/<conf>/`.

### 7.5 Краш-лог
`lytic_crashlog(handler, command=None, comment=None)`:
- номер = `len(ERRORS)+1`, файл `faillog/error[N][...].crash`;
- если бот подключён — шлёт BOSS сообщение «Ошибку смотри: "ошибка N", "sh cat ..."`.

---

## 8. Обработка станз

### 8.1 `MESSAGE_PROCESSING(client, stanza)` — на каждый `<message>`
Пошагово:
1. `fromjid = stanza.getFrom()`, `instance = fromjid.getStripped().lower()` (инстанс комнаты), `INFO['msg']+=1`.
2. Для `@conference` / при наличии `<result>` пишется строка в `dynamic/msg_log.txt`.
3. `user_level <= -100` → игнор (`NodeProcessed`).
4. Если `instance in UNAVALABLE and not MSERVE` → игнор.
5. **MAM**: если есть `<result>` и есть `MAM_HANDLERS` → запустить все `MAM_HANDLERS(stanza, fromjid, instance)` потоками и вернуться.
6. **Timestamp** (есть `<delay>`/`<x jabber:x:delay>`): если сейчас в окне `CONF_HISTORY_UNTIL[instance]` — `CONF_HISTORY[instance]+=1`; игнор (история не обрабатывается).
7. Своя станза (ник == `handler_botnick`) — игнор.
8. `body = stanza.getBody().strip()`.
9. **Ростер-фильтр** для не-конференций: если в `RSTR['BAN']` или `RSTR['VN']=='off'` — игнор; если `VN=='iq'` и не в `RSTR['AUTH']` — запуск `roster_check` (IQ-верификация) и игнор.
10. Обрезка `body[:INC_MSG_LIMIT]`.
11. Определение `type`: `'groupchat'`→`'public'` (обновляет `idle`), `'error'`→обработка, иначе `'private'`.
12. **Flood-контроль**: запускается поток `flood_timer(fromjid, instance, nick)`.
13. Разбор:
    - удаляет `BotNick:` / `BotNick,` / `BotNick>` из `combody`;
    - `rcmd = combody.split()[0].lower()`;
    - если команда в `COMMOFF[instance]` — игнор;
    - `cbody = MACROS.expand(combody, [fromjid, instance, nick])` (расширение макро);
    - `command = cbody.split()[0].lower()`;
    - префиксная логика: если есть `PREFIX[instance]`, удаляет префикс `!,@,#,.,*,+,``;
    - `Parameters = cbody[после первого пробела].strip()`.
14. Если `command in COMMANDS` → **`call_command_handlers(command, type, [fromjid,instance,nick], str(Parameters), rcmd)`**; иначе → `call_message_handlers(stanza, type, [fromjid,instance,nick], body)`.

**Спец-фикс MAM-триггера**: для команд `'чисть_мам'`/`'чистьмам'` из станзы берётся
`<stanza-id xmlns='urn:xmpp:sid:0' by=conf id=...>` (fallback `<archived id>`) и кладётся
в `LAST_MAM_TRIGGER_SID[instance]` — чтобы позже исключить сам триггер из удаления.

### 8.2 `call_command_handlers` (цепи)
- `call_command_handlers(command,typ,source,body,callee)`:
  - если конф не в `AFOOLS` и не в `PRIVATE_TYPE` → `call_command_handlers1`;
  - если в `PRIVATE_TYPE` → отвечать «---» и выполнять как `private` через `call_command_handlers3`;
  - если в `AFOOLS` (функ-фильтр «дураки») — с вероятностью 1/4 ругается, иначе `call_command_handlers1`.
- `call_command_handlers1` (основной путь):
  - `real_access = MACROS.get_access(callee, conf)`; если <=0 → `COMMANDS[command]['access']`;
  - `if has_access(source[0], real_access, conf):` запуск handler-потока, `COMMSTAT[command]['col']+=1`, записывает jid в `users`;
  - иначе — отказ (в `POL_SEX` — сухой отказ, иначе — случайная шуточная фраза).

### 8.3 `PRESENCE_PROCESSING(client, stanza)` — на каждый `<presence>`
1. `conf = fromjid.getStripped().lower()`.
2. `has_access(fromjid, -5, conf)` — иначе игнор.
3. `subscribe` → `roster_subscribe(conf)`.
4. Если `conf in GROUPCHATS`, `nick = fromjid.getResource()`:
   - **`unavailable`**:
     - `reason = getReason() or getStatus()`; `ishere=False`;
     - код `301/307` и ник — бот: `leave_groupchat`, доклад BOSS;
     - код `303` (смена ника): переносит данные `GROUPCHATS[conf][nick]→[Nick]`, `call_newnick_handlers(conf, nick, Nick)`;
     - иначе — `call_leave_handlers(conf, nick, reason, scode)`; чистит `idle/full_jid/joined`.
   - **`available` / `None`**:
     - JID: если нет `full_jid` → при `MSERVE` заносит конф в `UNAVALABLE`; иначе отказ;
     - обновляет `GROUPCHATS[conf][nick]`: `{role, caps, full_jid, jid, join_date, idle, joined, ishere}`;
     - `calc_acc(conf, jid, role)`;
     - если новый участник → `call_join_handlers(conf, nick, role[1], role[0], status, text)`;
     - если сменилась роль → `call_newrole_handlers`;
     - иначе → `call_newstatus_handlers`.
   - **`error`**: коды 409 (ник конфликтует → бот переименовывается: `BOT_NICKS[conf] = nick+'.'`, переподключение), 401/403/405 (выход), 404/503 (ре-join через 360с).
   - в конце — `call_presence_handlers(stanza)`.

### 8.4 `IQ_PROCESSING(client, iq)` — на каждый `<iq>`
- `INFO['iq']+=1`; игнор при `user_level <= -100`.
- Тип `get` → `buildReply('result')`:
  - `NS_VERSION`: name=Astra, version=`"%d (r.%d)"%(BOT_VER,BOT_REV)`, os=os_name;
  - `NS_URN_TIME`: tzo+utc;
  - `NS_DISCO_INFO`: identities/client+Astra + features (список NS_*);
  - `NS_LAST`: seconds + LAST['cmd'];
  - `NS_TIME` (xep-0090): utc/tz/display.
- Отправляет ответ и возвращается; иначе — `call_iq_handlers(iq)`.

---

## 9. Namespace'ы и XEP'ы

Определены в `xmpp.py`:

| Константа | Значение | XEP |
|---|---|---|
| `NS_CLIENT` | `jabber:client` | — |
| `NS_VERSION` | `jabber:iq:version` | XEP-0092 |
| `NS_ROSTER` | `jabber:iq:roster` | XEP-0065/02 |
| `NS_TIME` | `jabber:iq:time` | XEP-0090 |
| `NS_LAST` | `jabber:iq:last` | XEP-0012 |
| `NS_PRIVACY` | `jabber:iq:privacy` | XEP-0016 |
| `NS_REGISTER` | `jabber:iq:register` | XEP-0077 |
| `NS_VCARD` | `vcard-temp` | XEP-0054 |
| `NS_AUTH` | `jabber:iq:auth` | XEP-0078 |
| `NS_DISCO_INFO/ITEMS` | `...#disco#info`, `...#disco#items` | XEP-0030 |
| `NS_MUC` | `http://jabber.org/protocol/muc` | XEP-0045 |
| `NS_MUC_USER/ADMIN/OWNER/ROOMCONFIG` | `...#muc#user/admin/owner/roomconfig` | XEP-0045 |
| `NS_CAPS` | `http://jabber.org/protocol/caps` | XEP-0115 |
| `NS_DATA` | `jabber:x:data` | XEP-0004 |
| `NS_TIME_X` / `NS_URN_DELAY` | `jabber:x:delay` / `urn:xmpp:delay` | XEP-0091/0203 |
| `NS_URN_TIME` | `urn:xmpp:time` | XEP-0202 |
| `NS_PING` | `urn:xmpp:ping` | XEP-0199 |
| `NS_RECEIPTS` | `urn:xmpp:receipts` | XEP-0184 |
| `NS_XHTML_IM` | `http://jabber.org/protocol/xhtml-im` | XEP-0071 |
| `NS_MAM` | `urn:xmpp:mam:2` | XEP-0313 |
| `NS_RSM` | `http://jabber.org/protocol/rsm` | XEP-0059 |
| `NS_FORWARD` | `urn:xmpp:forward:0` | XEP-0297 |
| `NS_SID` | `urn:xmpp:sid:0` | XEP-0359 |
| `NS_MODERATE` | `urn:xmpp:message-moderate:1` | XEP-0425 |
| `NS_RETRACT` | `urn:xmpp:message-retract:1` | XEP-0424 |
| `NS_FASTEN` | `urn:xmpp:fasten:0` | XEP-0422 |
| `NS_MODERATE_0` / `NS_RETRACT_0` | legacy `...:0` | (старый ejabberd) |

Имена XEP'ов из `extensions/features.py` (фичи XMPP бота): версия, время, disco,
muc, ping, roster, vcard, x-data, last.

---

## 10. Глобальные реестры и словари

### 10.1 Реестры хендлеров (списки функций)
`IQ_HANDLERS`, `JOIN_HANDLERS`, `LEAVE_HANDLERS`, `NEWROLE_HANDLERS`,
`NEWSTATUS_HANDLERS`, `NEWNICK_HANDLERS`, `MESSAGE_HANDLERS`, `MAM_HANDLERS`,
`OUTGOING_MESSAGE_HANDLERS`, `PRESENCE_HANDLERS`; стадии `STAGE0..3_INIT`.

### 10.2 Словари состояния
см. таблицы AGENTS.md §3.2 + `COMMOFF`, `COMMSTAT`, `RUNTIMES`, `BOT_NICKS`,
`STATUS`, `CONF_HISTORY(_UNTIL)`, `MACROS`, `PRIVATE_TYPE`, `AFOOLS`, `POL_SEX`, `TENT`.

### 10.3 Механизм регистрации
Функция `register_<kind>_handler(instance)` удаляет из реестра функцию с тем же
`instance.__name__` и добавляет новую в конец. То есть повторная загрузка плагина
заменяет обработчик, а не плодит дубли. `call_*_handlers` создают по потоку на handler.

---

## 11. Система прав и доступов

### 11.1 Уровни доступа
| Уровень | Значение |
|---|---|
| 100 | суперадмин / BOSS |
| 80..99 | глобальный админ (в ADLIST) |
| 20 | админ |
| 15 | модератор |
| 10 | обычный участник (по умолчанию) |
| 5 | участник (из роли admin/member) |
| 1 | member-аффилиация |
| 0 | нет доступа |
| -100 | игнор (бан сообщений) |

### 11.2 `user_level(source, conf)`
```
level = 10
if jid in GLOBACCESS:     level = GLOBACCESS[jid]
elif jid in CONFACCESS[conf]: level = CONFACCESS[conf][jid]
elif jid in ACCBYCONF[conf]:  level = ACCBYCONF[conf][jid]
```
(Приоритет: глобальный > конференционный > per-conf имена.)

### 11.3 `calc_acc(conf, jid, role)`
`Roles = {'owner':15,'moderator':15,'participant':10,'admin':5,'member':1}`;
`access = Roles.get(affiliation,0) + Roles.get(role,0)`; применяет `change_local_access`,
**только если** jid не в `GLOBACCESS` и не в `CONFACCESS[conf]`.

### 11.4 Управление
- `change_global_access(jid, level)` — записывает в `GLOBACCESS` и в файл.
- `change_local_access(conf, jid, level)` — `ACCBYCONF`.
- `form_admins_list()` — заносит в `ADLIST` jid с уровнем >= 80.
- `has_access(source, level, conf)` = `user_level >= int(level)`.

---

## 12. Плагинная система

### 12.1 Загрузка (`load_plugins`)
- файлы `extensions/*.py`;
- маркеры по первым ~20 байтам: `# BS mark.1` (82 файла, BlackSmith-плагины) и `talis` (129, Talisman);
- иначе — не загружается (список в «There are N unloadable plugins»);
- `execfile(filename, globals())` — плагин исполняется с правами ядра.

### 12.2 Регистрация команд

**Talisman (новый):**
```python
command_handler(handler, access, "plug_name")
# имя команды берётся из help/plug_name по ключу handler.__name__ -> ["cmd"]
```

**BlackSmith (старый):**
```python
register_command_handler(handler, 'команда', [], access, desc, syntax, examples)
```

Общий реестр: `COMMANDS[command]={'plug':plug,'access':access}` (у Talisman)
или `{'desc':...,'syntax':...,'examples':[...]}` (у BlackSmith); `COMMAND_HANDLERS[command]=handler`.

### 12.3 Сигнатура командного хендлера
```python
def handler(type, source, body):
    # type: 'public' | 'private'
    # source = [full_jid, conf, nick]
    # body   = строка параметров (без имени команды)
```

### 12.4 Стадии инициализации
- `register_stage0_init(fn)` — после подключения (без комнат).
- `register_stage1_init(fn)` — на вход в каждую комнату (`fn(conf)`).
- `register_stage2_init(fn)` — после входа во все комнаты.
- `register_stage3_init(fn)` — перед выходом/рестартом.

### 12.5 Ответы бота
- `reply(type, source, text)` — публично с обращением по нику (`nick, text`), в приват — `msg(source[0], text)`; учитывает `A_NAME` (замену ника-обращения).
- `msg(target, body)` — отправить станзу; обрезает длинные (`CHAT_MSG_LIMIT`/`PRIV_MSG_LIMIT`, мульти-части `[1/N]`).
- `delivery(text)` — доставить BOSS в приват.

### 12.6 Признаки / структура help
Каждый Talisman-плагин обычно пишет `command_handler(x, access, "plug")` и требует
`help/plug` (python-dict) с ключами `cmd`, `syntax`, `examples`, `desc`.

---

## 13. Макросистема

`macros.py` — класс `Macros`.

### 13.1 Препроцессор команд
- `MACROS.expand(command, source)` — расширяет макро/алиасы в команде (глобальные и per-конфа).
- Синтаксис: `$1..` — аргументы; `$*` — все аргументы; `%(command, a, b)` — макрокоманда.
- Разделители: пробел, обратный слеш для экранирования, обратные кавычки для группировки («larg»).
- Макрокоманды: `rand`, `shell_escape`, `xml_escape`, `context(conf|nick|conf_jid)`.

### 13.2 Данные
- глобальные макро: `dynamic/macros.txt`, `dynamic/macroaccess.txt`;
- per-конфа: `dynamic/<conf>/macros.txt`, `dynamic/<conf>/macroaccess.txt`.
- доступ к макро — `get_access(macro, conf)`; `give_access(macro, access, conf)`.

Плагины, работающие с макро: `alias.py`, `alias_plugin.py`, `acmd.py`, `macro.py`,
`macro1.py`, `macrokill.py`.

---

## 14. Справочная система (help)

Каталог `help/<plug>` — это Python-dict, сериализованный через `str()/eval()`.
Ключи на имена хендлеров. Пример (`help/collect`):

```python
{
 u"handler_clean_mam": {
    u"syntax":   u'''чисть_мам [ник] [число]''',
    u"cmd":      u'''чисть_мам''',
    u"examples": [u'''чисть_мам''', u'''чисть_мам rain 10'''],
    u"desc":     u'''Удаляет через MAM (XEP-0425) ...'''
 },
 ...
}
```

- `command_handler(handler, access, "plug")` читает `load_file("help/%s"%plug,{})[handler.__name__]["cmd"]`.
- `command_help` (плагин help) выводит `desc`, `syntax`, `examples`, требуемый уровень.
- `help/commands` — категория `*`.

---

## 15. Персистентность данных

- **Текстовые python-контейнеры**: базы команд/плагинов лежат в `dynamic/*.txt` как `str(dict)`; читаются `load_file` (через `eval`), пишутся `write_file`.
- **Динамика комнат**: `dynamic/<конфа>/*.txt`; имя кодируется `enconf.chkFile` (юникод-часть в hex).
- **Immutable**: `static/*.txt` (тексты, вопросы, статусы, базы данных), `static/versions.py` (BOT_VER/CORE_MODE/BOT_REV).
- **БД** — опционально через `itypes.Database` (обёртка sqlite3).
- **Логи конференций** — плагин `logger` (+ темы в `static/logger/themes`).

### 15.1 `enconf.chkFile`
- заменяет `\t\n\r` на экранированные;
- если в имени >1 слеша и есть не-ASCII — `nameEncode` hex-кодирует юникод-часть.
- `chkUnicode(body)` — проверяет, все ли символы ASCII-таблицы.

---

## 16. Сетевые и утилитные модули

### `webtools.py`
- `read_url(link, Browser=None)` — через `requests`, с прокси и таймаутом; `decode_page` (utf-8/cp1251/...).
- `uHTML(data)` — HTML-unescape + замена `<br>`.
- `stripTags`, `getTagData`, `getTagArg`, `re_search`.
- `IDNA(text, encode)` — punycode домена.
- `byteFormat(size)` — человекочитаемый размер.
- `UserAgents` (`OperaMini`, `Firefox`, `BlackSmith`).

### `itypes.py`
- `Number` — счётчик (`plus`, `reduce`, int/str/float/repr).
- `Database(filename)` — обёртка sqlite3 (`execute`, `commit`, `fetch*`, context manager).

### `pattern.py`
- `Pattern` (базовый, `*` = любое), `JIDPattern` (`*.@*.com/*`), `NickPattern`.

### `sTools.getArchitecture()` — `[x86_64]` из `os.uname()[4]`.

### `simplejson.py` — реэкспорт `json`.

---

## 17. MUC-жизненный цикл и роли

- Вступление: `join_groupchat(conf, nick, code)` → записывает конфу в `GROUPCHATS_FILE`, шлёт presence с `<history maxstanzas=>` и кодом; запускает stage1.
- `GROUPCHATS[conf][nick]` поля:
  `jid`, `full_jid`, `role` (аффилиация, роль), `caps`, `ishere` (bool), `idle`,
  `joined`, `join_date` (`(date_int, time_struct)`).
- Роли/аффилиации из `<item role=.. affiliation=..>`; `calc_acc` переводит в уровень.
- Кик/бан/роли — `handler_iq_send(...)` с запросами `<query xmlns='muc#admin'><item .../>`.
- Управление командами: `handler_kick/handler_ban/handler_admin/handler_owner/handler_moder/...`.

---

## 18. MAM/Архив (XEP-0313) и модерация (XEP-0425)

Реализация — в `extensions/collect.py` (плагин `collect`).

### 18.1 Поток данных
1. **Триггер** — команда `чисть_мам [ник] [число]` (BlackSmith-регистрация уровня 15).
   В ядре `MESSAGE_PROCESSING` для этой команды из станзы извлекается её `stanza-id` (XEP-0359)
   → `LAST_MAM_TRIGGER_SID[conf]`.
2. `_mam_start(conf, nick, limit, mType, source, exclude_sid)`:
   - `qid = "mam-c-<seq>"`, `fetch_max = max(limit*3, limit+20)`;
   - `MAM_COLLECT[qid] = {conf, nick, limit, mType, source, exclude_sid}`;
   - шлёт IQ `<query queryid=qid xmlns='urn:xmpp:mam:2'>` с `<x type=submit>`
     (FORM_TYPE=NS_MAM), `<set><max>fetch_max</max><before/></set>` (RSM по последней странице);
   - `SendAndCallForResponse(iq, _mam_fin_answer, {'qid':qid})`.
3. **Результаты** — `handler_mam_result(stanza, fromjid, instance)`, зарегистрирована
   в `MAM_HANDLERS`. Разбирает `<forwarded><message><stanza-id .../>`; извлекает ник из
   `from/<resource>` и `sid`; не учитывает сообщения бота и сам триггер
   (`sid == exclude_sid`); складывает `(sid, nick)` в `MAM_RESULTS[qid]`.
4. `_mam_fin_answer(coze, stanza, qid)`:
   - ждёт 1с (доставка результатов), читает `MAM_RESULTS.pop(qid)`;
   - фильтрует по нику, режет `[-limit:]`;
   - для каждой записи `_mam_send_moderate(conf, sid)`.

### 18.2 `_mam_send_moderate(conf, stanza_id)`
```
<iq type='set' to=conf id='mam-mod-N'>
  <moderate id='<sid>' xmlns='urn:xmpp:message-moderate:1'>
    <retract xmlns='urn:xmpp:message-retract:1'/>
    <reason>Moderated via чисть_мам</reason>
  </moderate>
</iq>
```
(Режим `MAM_USE_LEGACY` → `apply-to`/`fasten:0` со старыми moderation-вариантами.)

### 18.3 Глобальные
`MAM_COLLECT`, `MAM_RESULTS`, `LAST_MAM_TRIGGER_SID`, `MAM_SEQ`, `MAM_USE_LEGACY`,
`MAM_RSM_BEFORE`, `MAM_DEBUG_FILE`.

**Ключевое**: станзы-результаты MAM не порождают событие `message` slixmpp, потому
ловит их низкоуровневый `legacy_message` колбэк `_on_message_low` в `xmpp.py`.

---

## 19. Ошибки, краши, перезапуск

- `lytic_crashlog(handler, command, comment)` — асинхронный краш-лог в `faillog/error[N].crash`, номер `len(ERRORS)+1`, доклад BOSS.
- `Dispatch_handler` ловит: `Conflict` (рестарт), `SystemShutdown/IOError` (реконнект `Connect`+`join_chats`), `StreamError`, `ExpatError`, `KeyboardInterrupt` (`sys_exit`).
- `Dispatch_fail` — ошибка разбора станзы: `.crash` в `__main__.crash`, инкремент `INFO["errs"]`, доклад BOSS.
- Автоперезапуск при > 600 ошибок (`INFO['errs'] > 600`) или `NoIqAnswer`/`IOError`.
- `upkeep()` — цикл каждые 60с: `gc.collect()`, при `MEMORY_LIMIT` и превышении RSS → `sys_exit('memory leak')`;
  запускается в `starting_actions()`.

---

## 20. Тесты и диагностика

| Скрипт/механизм | Назначение |
|---|---|
| `tests/test-load.py` | проверяет загрузку всех плагинов (compile+exec в `astra.__dict__`) |
| `tests/mam_diag.py` | одноразовая диагностика MUC MAM (slixmpp xep_0313/xep_0059) |
| `dynamic/raw_log.txt` | сырые станзы при открытом окне `_raw_log_open_window` |
| `dynamic/msg_log.txt` | строки `MP enter ...` из `MESSAGE_PROCESSING` |
| `dynamic/mam_debug.txt` | журнал MAM-операций (`_mam_log`) |
| `faillog/error[N].crash` | crash-файлы |
| `PID.txt` | PID + статистика рестартов |

Запуск тестов загрузки: `python3 tests/test-load.py`.

---

## 21. Полный каталог плагинов

> Легенда: **BS** — BlackSmith (`# BS mark.1`), **TL** — Talisman (`talis`).
> Ниже перечислены файлы `extensions/*.py` с кратким описанием и командами.

### Игры и развлечения
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `27_tup_plugin.py` | TL | `туп` | Гадание («туп») |
| `bandit.py` | TL | `бандит` | Игра «Бандит» |
| `bomba.py` | TL | `бомба` | Игра «Бомба» |
| `bottle.py` | BS | `бутыль`, `бутыль*` | Игра в бутылочку |
| `buket.py` | BS | `букет`, `бухло` | Дарит цветы/бухло |
| `chai.py` | TL | `чай` | Чаепитие |
| `chislo.py` | TL | `число` | Игра «Число» |
| `delirium.py` | TL | `тык`, `тык*` | Тыкание участника |
| `drink.py` | TL | `выпить` | Выпить в баре |
| `duel.py` | TL | `дуэль` | Дуэль между участниками |
| `elka.py` | TL | `ёлка` | Ёлка в конфе |
| `fun.py` | TL | `живу` | «Живу» (статус) |
| `fun1.py` | TL | `поэма` | Случайная поэма |
| `garniz.py` | TL | `гарнизон` | Стратегическая игра «Гарнизон» |
| `gorog_m.py` | TL | `купить` | Покупки в городе |
| `igra.py` | TL | `рейтинг,старт,дать,здания,построить,склады,игроки` | Стратегическая игра с ресурсами |
| `kafeta.py` | TL | `кафета` | Кафетерий |
| `kofe_plugin.py` | TL | `кофе` | Кофе |
| `millionaire_plugin.py` | TL | `!миллионер`, `!подсказка` | Игра «Миллионер» |
| `ochko21.py` | TL | `очко` | Игра «Очко» (21) |
| `opros.py` | BS | `опрос,пункты,вариант,вариант*` | Опросы |
| `podarok.py` | TL | `подарок` | Подарить подарок |
| `pokysai.py` | TL | `покусай`, `атата` | «Покусать» |
| `quiz.py` | TL | `викторина,игра,ответ,счет,...` | Викторина с очками |
| `roulette.py` | TL | `рулетка` | Русская рулетка |
| `rr_plugin.py` | TL | `рр,ррстарт,рррег,ррстат,...` | Игра «Русская рулетка» (с регистрацией) |
| `seabatl_plugin.py` | TL | `мор_бой` | Морской бой |
| `sex_plugin.py` | TL | `секс` | Юмористическая «секс-статистика» |
| `sekasa_plugin.py` | TL | `тык_всех` | Тыкать всех |
| `sekas_plugin.py` | TL | `групповуха` | Массовая «групповуха» |
| `sekasb_plugin.py` | TL | `поцелуй_всех` | Поцеловать всех |
| `snow_plugin.py` | TL | `!снежки`, `!snowballs`, `top,a,br` | Снежки (сбор и бросок) |
| `strategiya.py` | TL | `стратегия` | Стратегия |
| `strelka.py` | TL | `следи`,`неследи` | Слежение за ником |
| `taro.py` | TL | `таро,1,2,3,0` | Расклад Таро |
| `tictactoe_plugin.py` | TL | `хо-старт,хо-стоп,хо-счет,хо-помощь` | Крестики-нолики |
| `vote.py` | TL | `голосование,голосование*,мнение,пункт,итоги` | Голосования |
| `uzver.py` | TL | — | Зверь (утилита) |
| `kiss_plugin.py` | TL | `поцелуй` | Поцелуй |
| `karma_plugin.py` | TL | `карма`, `карма_детали` | Карма участников |
| `duel.py` | TL | `дуэль`, `ecipirovka` | Дуэль |

### Модерация, безопасность, права
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `access.py` | BS | `глобдоступ,логаут,локдоступ,доступ,логин` | Уровни доступа |
| `access_plugin.py` | TL | `доступ`, `access` | Доступ по ролям |
| `acclist.py` | BS | `доступы`, `доступы*` | Список доступов |
| `admin.py` | BS | `джойн,реджойн,префикс,таймап,ботап,рестарт,свал,выкл,ошибка,комстат,1..4,0` | Админ-команды |
| `admin_pl.py` | TL | `!джойн,!реджойн,!свал,!рестарт,!выкл, префикс` | Админ (Talisman) |
| `antibot.py` | BS | `исключения` | Исключения антибота |
| `antispace.py` | BS | `антиспэйс` | Запрет пробелов в никах |
| `antispamer.py` | BS | `спамеры` | Бан серверов спамеров |
| `antivipe_plugin.py` | TL | `антивайп`, `!спамсерв`, `бансерв` | Защита от вайпа |
| `automember.py` | BS | — | Авто-мембер по правилам |
| `autoroles.py` | BS | `акик,авизитор,амодер` | Авто-роли |
| `botstatus.py` | BS | `ботстат` | Статус бота |
| `captcha_plugin.py` | TL | `капча,капча_ав,капча_жид,капча_конфиг` | CAPTCHA (проверка людей) |
| `commoff.py` | TL | `отключить`,`включить` | Отключение команд в конфе |
| `invite_plugin.py` | TL | `!призвать` | Приглашение |
| `iq_filter.py` | TL | `мук` | Мук-фильтр сообщений |
| `mucacc.py` | BS | `бан,модер,кик,визитор,овнер,никто,фулбан,фулунбан,админ,мембер,участник,тапки,девойс,войс` | MUC-администрирование |
| `nakaz_plugin.py` | TL | `наказать` | Наказание |
| `order.py` | TL | `ордер` | Фильтры для конференции |
| `privacy_plugin.py` | TL | `privacy,privacy_edit,!f` | Приват-листы |
| `roster.py` | BS | `ростер`,`ростер*` | Ростер-фильтр |
| `spisok_afl_plugin.py` | TL | `список`,`!банлист` | Список аффилиаций |
| `stanza.py` | TL | `станза` | «топка» станз |
| `superamoder.py` | BS | `автобосс` | Авто-суперадмин→модератор |
| `verification.py` | BS | `авторизация` | Проверка «бота» |
| `vcard_plugin.py` | TL | `визитка`, `вчек`, `юзеринфа` | vCard |
| `virus_plugin.py` | TL | `скан`,`тест`,`test` | Сканер/защита |
| `zona_plugin.py` | TL | `опустить`,`опустить*` | Зона (роли) |
| `zvanie.py` | TL | `звание+`,`звание-` | Звания участников |
| `spam.py` | TL | `спамжид` | Спам-фильтр |
| `spam_private__plugin.py` | TL | `смайл` | Смайл-спам |
| `spamjidi_plugin.py` | TL | `.спамжид`,`.спамжид_серв` | Отправка спама |

### Команды, макро, плагины
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `acmd.py` | TL | `.алиас`, `acmd_*` | Алиасы команд |
| `alias.py` | TL | `алиас,макролист,макродел` | Алиасы |
| `alias_plugin.py` | TL | `alias_help,alias_msg,alias_join` | Алиасы событий |
| `cmds_plugin.py` | TL | `.ком`, `нулл`, `!нулл` | Псевдо-команды |
| `commands.py` | BS | `*` | Выполнение до 4 команд |
| `extmanager.py` | BS | `пм` | Менеджер плагинов |
| `find_cmd.py` | BS | `плагин` | Поиск плагина по команде |
| `macro.py` | BS | `макро,глобмакро,макролист,макродоступ` | Макро |
| `macro1.py` | BS | `макролист+` | Макро (вариант) |
| `macrokill.py` | BS | `ботник,топик,хтобыл,хдея,чатлист` | Макро-утилиты |
| `macrosyi_pl.py` | TL | `торт,босса,арбуз,бабу,...` | Макро-конфетки |
| `newcmd.py` | TL | — | Новая команда |
| `plugin.py` | BS | `подгрузи,комаут,комадд,плаглист` | Плагины |
| `recmd.py` | BS | `заменить` | Переопределение команд |
| `remote-ctrl.py` | BS | `ремоут` | Дистанционное управление |
| `send1.py` | TL | — | Отправка |
| `more.py` | TL | `далее` | Продолжение сообщения |
| `most.py` | TL | `мост`,`мост_дел` | Мост между конфами |
| `everywhere.py` | BS | `везде` | Команда во всех конферах |
| `presence_plugin.py` | TL | — | Обработка presence плагина |

### Утилиты и сеть
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `google.py` | BS | `гугл` | Поиск Google |
| `gde.py` | TL | `гдея` | Где я (геолокация) |
| `gorod.py` | TL | `#` | Город |
| `wiki.py` | BS | `вики` | Поиск по Wikipedia |
| `usearch.py` | BS | `us` | usearch |
| `userch.py` | BS | `ищи` | Поиск юзера |
| `userseach_plugin.py` | TL | `disco_ans`,`отыскать` | Поиск юзера по disco |
| `usersearch.py` | TL | `!отыскать`,`отыскать` | Поиск юзера |
| `userinfa.py` | BS | `юзеринфа` | Авто-вскрытие vCard новичков |
| `userstat.py` | BS | `пребывание`,`юзерстат` | Статистика юзера |
| `talkers.py` | BS | `трёп` | Статистика болтунов |
| `statconfs.py` | BS | `посещаемость` | Посещаемость конференций |
| `servres.py` | BS | `сервера`,`ресурсы` | Топ серверов/ресурсов |
| `raiting.py` | BS | `рейтинг` | Рейтинг jc |
| `infa.py` | TL | `инфа` | Статистика сервера |
| `info.py` | TL | `инмук,тружид` | Количество юзеров |
| `info_plugin.py` | TL | `банверсия+,банверсия-,потоки,тружид,инмук,ботап+` | Инфо |
| `jabberq_plugin.py` | TL | `!цитата`, `!цитата+` | Цитаты |
| `seen_plugin.py` | TL | `видели` | Когда видели |
| `idle_plugin.py` | TL | `аптайм`,`жив` | Время неактивности |
| `status.py` | TL | `статус` | Статус юзера |
| `networktime.py` | BS | `куранты` | Точное время |
| `time.py` | TL | `часики` | Время у юзера |
| `ping.py` | BS | `пинг`,`пингстат` | Ping |
| `pingturbo.py` | TL | `турбопинг` | Turbo ping |
| `pingx.py` | TL | `нетпинг` | Net ping |
| `dns.py` | BS | `днс`,`порт` | DNS/порт |
| `weather.py` | BS | `погода` | Погода |
| `trans.py` | BS | `перевод`,`!` | Переводчик |
| `trans.py___________` | BS | — | (запасной) |
| `turn.py` | BS | `турн`,`атурн` | Переключение раскладки |
| `uto-shortener.py` | BS | `урл` | Сокращение URL |
| `urldetect.py` | BS | `урлдетект` | Авто-заголовки ссылок |
| `temp.py` | BS | `температура` | Перевод градусов |
| `converter.py` | BS | `convert` | Конвертер |
| `distance.py` | BS | `расстояние` | Расстояние между городами |
| `price.py` | BS | `цена` | Стоимость домена |
| `file.py` | BS | `файл` | Создание файла |
| `download.py` | BS | `скачать` | Скачивание |
| `e-mail.py` | TL | `email` | Email |
| `newjid.py` | BS | `регжид` | Регистрация JID |
| `vcard.py` | BS | `визитка` | vCard |
| `privacy_plugin.py` | TL | `privacy` | Приват-листы |
| `disco.py` | BS | `диско` | Disco-обзор сервисов |
| `version.py` | TL | `версия` | Версия клиентов |
| `botversion.py` | TL | `шифруйся` | Имя версии бота |
| `svn_info.py` | BS | `свн` | Обновления в SVN |
| `interpreter.py` | BS | `калк,sh,exec,eval` | Калькулятор/интерпретатор |
| `cron.py` | BS | `хрон` | Cron-задачи |
| `timer.py` | BS | `таймер` | Таймер команд |
| `alarm.py` | BS | `напомнить` | Напоминания |
| `note.py` | BS | `блокнот` | Личный блокнот |
| `54_note.py` | TL | `запомнить,забыть,записи` | Блокнот (TL) |
| `holydays.py` | BS | `праздники` | Праздники |
| `new_year.py` | BS | `нг` | До нового года |
| `fact.py` | TL | `тлд` | География TLD |
| `referats_plugin.py` | TL | `реферат` | Реферат |
| `gotovim_plugin.py` | TL | `рецепт` | Рецепт |
| `tvru_plugin.py` | TL | `тв,тв_лист,тв_полностью,тв_найти` | ТВ-программа |
| `www_plugin.py` | TL | `www` | WWW-утилита |
| `xboltun.py` | BS | `голос` | Болталка |
| `wtf.py` | BS | `?`,`??`,`??все`,`??поиск`,`??эксп`, `!?`, `??лок`,`??глоб` | База определений |

### Коллекция/утилиты баз
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `collect.py` | BS | `чисть,чисть_мам,ласт,сказать,отменя,мессага,суперадмину,тест,блэклист` | Чистка конфы, MAM, глобальные сообщения |
| `collect1.py` | TL | `.тест` | Трассировка теста |
| `quotess*` | — | — | Цитаты |

### Справочные/справка
| Плагин | Тип | Команды | Описание |
|---|---|---|---|
| `help.py` | BS | `хелп,помощь,?,команды,комдоступ,комлист,1..8,0` | Справка |
| `help2.py` | BS | `комлист` | Список команд |
| `help_ef.py` | TL | — | Справка (EF) |
| `spravka_bot_plugin.py` | TL | `справка`,`хдебот` | Справка по боту |

---

## 22. Полный каталог справочных команд

> `help/<имя>` = python-dict с командами. Ниже — команды по плагинам, как их видит бот.

| Команда | Описание |
|---|---|
| **абсурд** | статья «Абсурдопедия» |
| **автобосс** | авто-смена суперадмина→модератора |
| **авторизация** | проверка новичка на бота |
| **акик/авизитор/амодер** | авто-роли (кик/визитор/модер) |
| **алиас/макролист/макродел** | пользовательские алиасы |
| **антивайп** | защита от вайп-атак |
| **антиспэйс** | запрет пробелов в никах |
| **аптайм/жив** | время неактивности |
| **блокнот** | личный блокнот |
| **бомба** | игра «Бомба» |
| **ботап/ботстат** | статус бота |
| **бан/модер/кик/визитор/овнер/никто/фулбан/фулунбан/админ/мембер/участник/тапки/девойс/войс** | MUC-роли (mucacc) |
| **блэклист** | чёрный список для «суперадмину» |
| **босса** | пригласить админа бота |
| **буклет/бухло** | дарить цветы/бухло |
| **бутыль** | игра в бутылочку |
| **везде** | команда во всех конфах |
| **визитка** | vCard юзера |
| **вики** | поиск по Wikipedia |
| **глобдоступ/локдоступ/логаут/доступ/логин** | уровни доступа |
| **голос** | болталка |
| **голосование/голосование*/мнение/пункт/итоги** | голосования |
| **гугл** | поиск Google |
| **джойн/реджойн/свал/выкл/рестарт/префикс/таймап/ботап/ошибка/комстат** | админ-команды |
| **далее** | продолжение обрезанного сообщения |
| **девойс/войс/тапки** | роль visitor/participant |
| **диско** | обзор сервисов |
| **днс/порт** | DNS/порт |
| **доступ/доступы** | доступ/список доступов |
| **доступы*** | список глобальных доступов |
| **дуэль** | дуэль |
| **живу/поэма** | развлечения |
| **заменить** | переопределение команды |
| **звание+/звание-** | звания |
| **игрушки (бандит/бомба/рулетка/очко/мор_бой/снежки/миллионер/викторина/крестики-нолики/таро/число/стратегия/гарнизон)** | игры |
| **инфа** | статистика сервера |
| **инмук/тружид** | число юзеров/реальный jid |
| **исключения** | антибот-исключения |
| **калк/sh/exec/eval** | калькулятор/интерпретатор |
| **календарь** | календарь |
| **карма/карма_детали** | карма |
| **капча/капча_ав/капча_жид/капча_конфиг** | CAPTCHA |
| **комгид/комлист/команды/хелп/помощь/комдоступ** | справка |
| **круанты** | точное время |
| **ласт** | последние сообщения конфы |
| **логгер/логгер*** | логирование |
| **макро/глобмакро/макролист/макродоступ** | макро |
| **мессага** | сообщение от бота |
| **мор_бой** | морской бой |
| **мост/мост_дел** | мост между конфами |
| **наказать** | наказание |
| **напомнить** | напоминание |
| **нетпинг** | net ping |
| **нг** | до нового года |
| **обаяние/обещаю** | обещания |
| **опрос/пункты/вариант** | опросы |
| **ордер** | фильтры конфы |
| **отключать/включить** | отключение команд |
| **отменя** | глобальное сообщение |
| **перевод/!** | переводчик |
| **передать** | передать сообщение нику |
| **пинг/пингстат/турбопинг** | ping |
| **плаглист/подгрузи/комаут/комадд** | управление плагинами |
| **погода** | погода |
| **подарок** | подарки |
| **построить/склады/здания/рейтинг/старт/дать/игроки** | стратегия |
| **праздники** | праздники |
| **пребывание/юзерстат** | статистика юзера |
| **превед/превед*** | приветствия |
| **призвать** | инвайт |
| **приват** | выполнить команду в привате |
| **просмотр/тв/тв_лист/тв_полностью/тв_найти** | ТВ |
| **пук** | сила звука пука |
| **ремоут** | дистанционное управление |
| **рецепт** | рецепт |
| **рейтинг** | рейтинг jc |
| **ростр/ростер*** | ростер-фильтр |
| **рулетка** | русская рулетка |
| **сброс** | сброс |
| **сервера/ресурсы** | топ серверов |
| **сказать** | говорить через бота |
| **скачать** | скачивание |
| **спамеры** | бан спам-серверов |
| **список/!банлист** | списки аффилиаций |
| **статус** | статус юзера |
| **станза** | «топка» |
| **суперадмину** | сообщение админу бота |
| **счет/викторина/игра/ответ/дальше/повтори/стой** | викторина |
| **смайл (спам_private)** | смайл-спам |
| **тамагочи (кушай/пей/играй/почитай/пойди/гигиена/состояние/холодильник/тамагочи/выпей)** | тамагочи |
| **таймер/хрон** | таймер/cron |
| **температура** | перевод градусов |
| **тест** | тест |
| **тлд** | география домена |
| **топик/ботник/хтобыл/хдея/чатлист** | макро-утилиты |
| **трёп** | статистика болтунов |
| **турн/атурн** | переключение раскладки |
| **тык/тык*** | тыкать |
| **удалить (удalit_plugin)** | удалить сообщение |
| **урл/урлдетект** | URL-утилиты |
| **цена** | стоимость домена |
| **часики/куранты** | время |
| **чисть/чисть_мам** | чистка конфы / чистка MAM |
| **шроника** | шифр |
| **юзеринфа** | авто-vCard новичка |
| **юзерстат** | статистика юзера |
| **этапize (privacy)** | приват-листы |
| **якорь/ый** | разное |

> Точный и актуальный список команд всегда выдаёт сам бот командой `команды` /
> справкой по конкретной команде (`помощь <команда>`).

---

*Готово. Полное техническое описание проекта «Astra».*
