# BS mark.1
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# BETA! 
import re
import requests
from urllib.parse import urlsplit, urlunsplit


def urlWatcher(raw, mType, source, body):
        if mType == "public" and (source[1] in urlDetect) and has_access(source[0], 11, source[1]):
                if len(body) < 500:
                        try:
                                m = re.search(r'https?://\S+', body)
                                url = m.group(0).strip(".,;:!?)]}\"") if m else ''
                                if url:
                                        if any(ord(c) > 0x7f for c in url):
                                                try:
                                                        _p = urlsplit(url)
                                                        _h = _p.hostname
                                                        if _h and any(ord(c) > 0x7f for c in _h):
                                                                _netloc = _h.encode("idna").decode("ascii")
                                                                if _p.port and _p.port != (443 if _p.scheme == "https" else 80):
                                                                        _netloc += ":" + str(_p.port)
                                                                url = urlunsplit((_p.scheme, _netloc, _p.path, _p.query, _p.fragment))
                                                except Exception:
                                                        pass
                                        _proxy = globals().get('NETWORK_PROXY')
                                        _timeout = globals().get('NETWORK_TIMEOUT', 20)
                                        proxies = {'http': _proxy, 'https': _proxy} if _proxy else None
                                        try:
                                                opener = requests.get(url, headers={'User-Agent': UserAgents['Firefox']},
                                                                      proxies=proxies, timeout=_timeout, stream=True)
                                                ContentType = opener.headers.get("Content-Type") or ""
                                                if "text/html" in ContentType or url.rstrip("/").endswith((".html", ".htm")):
                                                        data = b''
                                                        for chunk in opener.iter_content(65536):
                                                                data += chunk
                                                                if len(data) >= 2048576:
                                                                        break
                                                        data = decode_page(data)
                                                        title = getTagData("title", data)
                                                        answer = u"Заголовок: %s" % uHTML(title).replace("\n", "")
                                                else:
                                                        Type = ContentType
                                                        Size = byteFormat(int(opener.headers.get("Content-Length") or 0))
                                                        Date = opener.headers.get("Last-Modified") or ""
                                                        answer = u"Тип: %s, размер: %s; последнее изменение файла: %s." % (Type, Size, Date)
                                                opener.close()
                                                msg(source[1], answer)
                                        except requests.exceptions.RequestException:
                                                msg(source[1],u'не могу посмотреть инфу о ссылке. :(')
                        except Exception:
                            lytic_crashlog(urlWatcher, command="urldetect")
                            msg(source[1],u'не могу посмотреть инфу о ссылке. :(')

def urlWatcherConfig(mType, source, args):
        if args:
                if mType == "public":
                        args = args.strip()
                        if args == "1":
                                if source[1] in urlDetect:
                                        answer = u"Уже включено."
                                else:
                                        urlDetect.append(source[1])
                                        write_file("dynamic/urlWatcher.txt", str(urlDetect))
                                        answer = u"Включила автодетект ссылок."
                        elif args == "0":
                                if source[1] in urlDetect:
                                        urlDetect.remove(source[1])
                                        write_file("dynamic/urlWatcher.txt", str(urlDetect))
                                        answer = u"Выключила автодетек ссылок."
                                else:
                                         answer = u"Не включено."
                        else:
                                answer = u"Неизвестный параметр."
                else: 
                        answer = u"Только для чатов."
        else:
                answer = u"что?"
        reply(mType, source, answer)

def urlWatcherConfig_load():
        if initialize_file("dynamic/urlWatcher.txt", str(list())):
                globals()["urlDetect"] = load_file("dynamic/urlWatcher.txt", [])

register_message_handler(urlWatcher)
register_stage0_init(urlWatcherConfig_load)
command_handler(urlWatcherConfig, 20, "urldetect")