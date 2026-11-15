# Copy this file to config.py and set the connection credentials.

SERVER = 'example.org'
CONNECT_SERVER = SERVER
PORT = 5222
HOST = SERVER
SECURE = True
USERNAME = 'bot'
PASSWORD = 'change-me'
RESOURCE = u'astra'

DEFAULT_NICK = u'Astra'
CHAT_MSG_LIMIT = 4048
PRIV_MSG_LIMIT = 8960
INC_MSG_LIMIT = 8960
MSERVE = True
BOSS = 'owner@example.org'
MEMORY_LIMIT = 0

GLOBACCESS_FILE = 'dynamic/access.txt'
GROUPCHATS_FILE = 'dynamic/chats.txt'
QUESTIONS_FILE = 'static/veron.txt'
ROSTER_FILE = 'dynamic/roster.txt'
PLUGIN_DIR = 'extensions'
PID_FILE = 'PID.txt'

# Прокси и таймаут для сетевых запросов бота.
# Влияет на команды: погода, рецепт, тв, тв_полностью, тв_лист, тв_найти, реферат
# и автоопределение заголовков ссылок в конференциях.
# None или '' — без прокси.
NETWORK_PROXY = None
NETWORK_TIMEOUT = 20
WEATHER_RESPONSE_FILE = 'dynamic/weather-response.html'

# Проверять TLS-сертификат сервера. False — только для самоподписанных сертификатов.
TLS_VERIFY_CERTIFICATES = True

# Кнопки быстрого ответа XEP-0439 (urn:xmpp:tmp:quick-response) в меню бота.
QUICK_RESPONSE_BUTTONS = True

# Каталог публичных HTML-логов (spamjid и др.).
PUBLIC_LOG_DIR = 'logs'

# Секреты внешних сервисов. Заполняйте в config.py (он в .gitignore), не в этом файле.
EMAIL_USER = ''
EMAIL_PASSWORD = ''
JABBERQ_API_KEY = ''
