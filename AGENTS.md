# AGENTS.md — Архитектура проекта «Astra»

> Навигационно-архитектурный справочник для разработчиков и ИИ-агентов.
> Astra — форк командного бота **BlackSmith mark.1** (XMPP/Jabber), переведённый на **Python 3 + slixmpp 1.17** через слой совместимости с legacy-API `xmpppy`.
> Бот — многофункциональный администратор Jabber-конференций и развлекательный бот.

---

## 1. Обзор и назначение

Astra — бот для XMPP (Jabber) конференций (MUC). Он подключается к серверу, заходит в список комнат, следит за присутствием участников, обрабатывает текстовые команды и сообщения, управляет правами/ролями, ведёт статистику, реализует множество игр и утилит.

Ключевые свойства:
- **Два поколения плагинов** в одной экосистеме: «BlackSmith» (`# BS mark.1` в заголовке) и «Talisman» (`talis` в заголовке). Оба загружаются `execfile`'ом прямо в глобальные имена `astra`.
- **Наследие Python 2**: исходники писаны под py2; проект поддерживает совместимость алиасами (`basestring`, `unichr`, `unicode`, `file`) и shim-файлами (`simplejson.py` → `json`).
- **Слой `xmpp.py`** эмулирует старый API `xmpppy` поверх асинхронного `slixmpp`.

---

## 2. Структура каталогов

```
astra/
├── astra.py            # ЯДРО: событийный цикл, обработчики, загрузка плагинов, main()
├── xmpp.py             # Слой совместимости xmpppy <-> slixmpp 1.17, namespace'ы, Client
├── config.py           # Локальная конфигурация (в .gitignore, не коммитить)
├── config.example.py   # Шаблон конфигурации для копирования
├── enconf.py           # Кодирование имён конференций для путей на диске (chkFile/nameEncode)
├── itypes.py           # Утилиты: Number, Database (sqlite3)
├── sTools.py           # getArchitecture()
├── simplejson.py       # shim: legacy simplejson -> stdlib json
├── webtools.py         # Сетевые функции: read_url, uHTML, stripTags, IDNA, byteFormat...
├── pattern.py          # Pattern / JIDPattern / NickPattern — шаблоны c *
├── macros.py           # Система пользовательских макро/алиасов
├── fixpass.py          # Разовый скрипт-фиксатор py2->py3 для плагинов
├── config.py           # конфигурация бота
├── enconf.py           # кодирование имён
├── PID.txt             # служебный файл: PID + статистика рестартов
├── extensions/         # Плагины (209 .py файлов)
├── help/               # Справочные файлы команд (Python dict'ы), по одному на плагин
├── static/             # Иммутабельные данные: versions.py, question-базы, тексты, темы логов
├── dynamic/            # Живые данные: .txt базы, логи, макро, per-конференция каталоги
├── faillog/            # Crash-файлы ошибок #NN
├── logs/               # Логи конференций (от плагина logger)
├── tests/              # Диагностические/загрузочные скрипты (mam_diag.py, test-load.py)
└── __pycache__/        # (в .gitignore)
```

---

## 3. Ядро `astra.py`

### 3.1 Глобальные реестры хендлеров

Каждый реестр — список функций; регистрация одноимённой функцией `register_<kind>_handler` (при повторной регистрации одноимённый старый удаляется):

| Реестр | Сигнатура хендлера | Регистрация |
|---|---|---|
| `IQ_HANDLERS` | `(iq)` | `register_iq_handler` |
| `JOIN_HANDLERS` | `(conf, nick, afl, role[, status, text])` | `register_join_handler` |
| `LEAVE_HANDLERS` | `(conf, nick, reason, code)` | `register_leave_handler` |
| `NEWROLE_HANDLERS` | `(conf, nick, role, reason)` | `register_newrole_handler` |
| `NEWSTATUS_HANDLERS` | `(conf, nick, status, priority, text)` | `register_newstatus_handler` |
| `NEWNICK_HANDLERS` | `(conf, old_nick, nick)` | `register_newnick_handler` |
| `MESSAGE_HANDLERS` | `(stanza, ltype, source, body)` | `register_message_handler` |
| `MAM_HANDLERS` | `(stanza, fromjid, instance)` | `register_mam_handler` |
| `OUTGOING_MESSAGE_HANDLERS` | `(target, body, obody)` | `register_outgoing_message_handler` |
| `PRESENCE_HANDLERS` | `(prs)` | `register_presence_handler` |
| `COMMAND_HANDLERS` | `{command: handler}` | `command_handler(...)` / `register_command_handler(...)` |

Инициализация — по стадиям `STAGE0_INIT`…`STAGE3_INIT` (`register_stageN_init`): Stage0 — после подключения, Stage2 — после входа в комнаты, Stage3 — перед выходом/перезапуском.

### 3.2 Ключевые глобальные словари

| Имя | Назначение |
|---|---|
| `GROUPCHATS[conf]` | `{nick: {jid, full_jid, role, caps, ishere, idle, joined, join_date}}` |
| `STATUS[conf]` | `{'message':..., 'status':...}` статус бота в комнате |
| `BOT_NICKS[conf]` | ник бота в комнате (по умолчанию `DEFAULT_NICK`) |
| `ADLIST` | список jid-админов (уровень >= 80) |
| `GLOBACCESS[jid]`, `CONFACCESS[conf][jid]`, `ACCBYCONF[conf][jid]` | уровни доступа |
| `COMMANDS[command]` | `{'plug', 'access'}` (или `{'desc','syntax','examples'}`) |
| `COMMAND_HANDLERS[command]` | функция-обработчик команды |
| `COMMSTAT[command]` | `{'col': вызовов, 'users': []}` |
| `COMMOFF[conf]` | список отключённых команд в комнате |
| `PREFIX[conf]` | префикс команд (обычно `!`) |
| `MACROS` | объект `macros.Macros()` |
| `CONF_HISTORY[conf]`, `CONF_HISTORY_UNTIL[conf]` | окно истории при входе |
| `INFO` / `INFA` | счётчики статистики |
| `RSTR` | `{'AUTH':[], 'BAN':[], 'VN':'off'}` — ростерная верификация |
| `UNAVALABLE` | комнаты без прав админа |
| `ANSWER` | кэш ростерной IQ-проверки |

### 3.3 Потоки и семафоры

- `smph = threading.Semaphore(60)` — ограничивает число одновременно запускаемых хендлер-потоков.
- `wsmph` — сериализует запись файлов.
- Каждый вызов хендлера — отдельный поток через `call_*_handlers` → `execute_handler` → `Thread_Run`/`Try_Thr`; ошибки ловит `lytic_crashlog`.

### 3.4 Основной цикл (`main`)

```
main() -> PID-контроль -> starting_actions() -> Connect() -> call_stage_init(0)
       -> join_chats() -> play-thread -> call_stage_init(2)
       -> бесконечный цикл: Dispatch_handler(calc_Timeout())
```

- `Connect()` создаёт `xmpp.Client`, коннектится, авторизуется, регистрирует `MESSAGE_PROCESSING`/`PRESENCE_PROCESSING`/`IQ_PROCESSING`.
- `calc_Timeout()` подбирает паузу по числу комнат (8с при <=16, 0.2с при >=48).
- `sys_exit()` — штатный выход/перезапуск (unavailable, stage3, `os.execl`).

---

## 4. Слой XMPP `xmpp.py`

Эмулирует legacy-API `xmpppy` поверх `slixmpp`:

- **Namespace'ы** — константы `NS_*` (см. SPEC.md §9). Важные для последних работ: `NS_MAM = "urn:xmpp:mam:2"`, `NS_SID = "urn:xmpp:sid:0"`, `NS_RSM`, `NS_MODERATE`, `NS_RETRACT`, `NS_FASTEN`.
- **`Node`** — обёртка над `xml.etree.ElementTree`, дающая методы `getTag/getTags/getAttr/setTagData/addChild/getNamespace/getQueryNS/...`.
- **`Message/Presence/Iq`** — подклассы `Node` для станз.
- **`JID`** — разбор `node@domain/resource`, методы `getStripped/getResource/getNode/getDomain`.
- **`Client`** — основной класс:
  - `connect()`, `auth(jid, pass, resource)` — поднимает `slixmpp.ClientXMPP` в отдельном потоке с собственным `asyncio`-loop.
  - `RegisterHandler(ns, fn)` — диспетчер `message`/`presence`/`iq` для ядра.
  - `_on_message`, `_on_presence`, `_on_iq` — драйверы событий slixmpp → оборачивают станзу в `Node` и отдают диспетчеру.
  - `_on_message_low` — низкоуровневый `Callback("legacy_message")`, ловит `<message><result xmlns='urn:xmpp:mam:2'>` (эти станзы **не триггерят** событие `message` в slixmpp — ключевой фикс для MAM).
  - `SendAndCallForResponse(stanza, func, args, timeout)` — отправляет IQ и по `MatcherId(id)` вызывает `func` с ответом (в тайм-аут — с `None`).
  - `send()`, `sendInitPresence()`, `isConnected()`, `isTls()`, `Process()` (просто sleep).
  - `_raw_log`, `_raw_log_open_window` — отладка сырых станз в `dynamic/raw_log.txt`.

---

## 5. Обработка станз (ядро)

### 5.1 `MESSAGE_PROCESSING(client, stanza)`
Порядок:
1. JID/инстанс комнаты; счётчики; лог в `dynamic/msg_log.txt` для конференций.
2. Пользователь с `user_level <= -100` — игнор.
3. **MAM-результат** (`<result>` есть): если есть `MAM_HANDLERS` — запустить их и вернуться.
4. Timestamp-станзы (история) — увеличить `CONF_HISTORY`, не обрабатывать.
5. Свои сообщения бота — игнор.
6. Ростер-верификация / бан / джет.
7. Обрезка длины, flood-таймер, разбор команды/параметров через `MACROS.expand`.
8. Команда есть в `COMMANDS` → `call_command_handlers`, иначе → `call_message_handlers`.

### 5.2 `PRESENCE_PROCESSING`
- subscribe → `roster_subscribe`.
- unavailable: обработка kick (301)/ban (307)/nick (303), leave-хендлеры.
- available: регистрация/обновление участника в `GROUPCHATS`, join/newrole/newstatus-хендлеры, `calc_acc`.
- error: 409 (конфликт ника → бот переименовывается с точкой), 401/403/405 (выход), 404/503 (возврат через 360с).

### 5.3 `IQ_PROCESSING`
- `get`: version (Astra, `BOT_VER (r.BOT_REV)`, os_name), time, disco#info, last.
- после встроенных ответов — `call_iq_handlers(iq)`.

---

## 6. Система прав

- Уровни: 0 — нет, 10 — участник, 15 — модератор, 20 — админ, 100 — суперадмин/BOSS.
- `user_level(source, conf)`: `GLOBACCESS` > `CONFACCESS` > `ACCBYCONF`, по умолчанию 10.
- Роли MUC → уровень: owner/moderator=15, participant=10, admin=5, member=1 (функция `calc_acc`; считается, только если нет глобального доступа).
- `has_access(source, level, conf)` — проверка. `form_admins_list()` собирает `ADLIST` (уровень >= 80).

---

## 7. Плагинная система

### 7.1 Загрузка
`load_plugins()` сканирует `extensions/*.py`:
- `# BS mark.1` в первых байтах (82 плагина) — BlackSmith;
- содержит `talis` (129 плагинов) — Talisman;
- **каждый исполняется через `execfile(filename, globals())`** — код получает доступ ко всем глobal'ам ядра напрямую.

### 7.2 Регистрация команд — два стиля
- **Новый** (Talisman, предпочтителен): `command_handler(handler, access, "plug_name")` — имя команды берётся из `help/plug_name` по ключу `handler.__name__` → `["cmd"]`.
- **Старый** (BlackSmith): `register_command_handler(handler, 'команда', [], access, desc, syntax, examples)`.

### 7.3 Сигнатуры командных хендлеров
```python
def handler(type, source, body):
    # type: 'public' | 'private'
    # source = [full_jid, conf, nick]
    # body = строка параметров (без имени команды)
```
Ответ — `reply(type, source, text)` (публично с обращением) / `msg(target, text)` / `delivery(text)` (BOSS в приват).

### 7.4 Пример Talisman-плагина
```python
#===istalismanplugin===
# ~*~ coding: utf-8 ~*~
def my_cmd(t, s, p):
    reply(t, s, u'Привет, %s!' % s[2])
command_handler(my_cmd, 10, "mymod")   # + help/mymod с cmd='моямода'
```

---

## 8. Файлы, данные, утилиты

- Запись/чтение: `write_file`, `read_file`, `load_file` (часто `eval` python-структуры), `initialize_file`, `check_file`.
- Имена файлов конференций кодируются `enconf.chkFile`; по умолчанию лежат в `dynamic/<conf>/...`.
- Данные — в основном **текстовые Python-контейнеры** (`str(dict)` / `eval`) в `dynamic/*.txt`. Исключение — `itypes.Database` (sqlite3) и `static/logger/themes`.
- Сетевой доступ — `webtools.read_url` и др. (через `requests`, с `NETWORK_PROXY`/`NETWORK_TIMEOUT`).
- `macros.Macros` — расширение `%(...)` и `$1..`, глобальные и per-конфа макро из `dynamic/macros.txt`.

---

## 9. Отладка и диагностика

| Файл/механизм | Назначение |
|---|---|
| `dynamic/raw_log.txt` | сырые входящие станзы (окно открывается `JCON._raw_log_open_window(sec)`) |
| `dynamic/msg_log.txt` | лог `MESSAGE_PROCESSING` (строка `MP enter ...` на станзу из конфы) |
| `dynamic/mam_debug.txt` | лог операций MAM (плагин `collect.py`) |
| `faillog/error[N].crash` | crash-файлы, номера показывает команда `ошибка N` |
| `tests/test-load.py` | проверка, какие плагины загружаются |
| `tests/mam_diag.py` | одноразовая диагностика MAM |

---

## 10. Частые задачи при разработке

1. **Добавить команду** → хендлер `def cmd(t,s,p)`, файл `help/<plug>` с ключами `cmd/syntax/examples/desc`, регистрация `command_handler(cmd, access, "<plug>")`.
2. **Реакция на событие комнаты** → `register_join/leave/newrole/..._handler`.
3. **MAM/модерация** → `extensions/collect.py`: `handler_mam_result` (в `MAM_HANDLERS`), `_mam_start`, `_mam_send_moderate`; глобальные `MAM_COLLECT`/`MAM_RESULTS`.
4. **Доступ/права** → `has_access`, `user_level`, `change_global_access`.
5. **Состояние бота** → `change_bot_status`, `STATUS[conf]`.

> Полная техническая спецификация всех подсистем, констант, XEP'ов и полный каталог плагинов — в **SPEC.md**.
