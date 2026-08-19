# BS mark.1-55
# /* coding: utf-8 */
# © SaranskCity 2019

def AnecDote(mType, source, body):
        if body == 'новинка':
                link='https://pda.anekdot.ru/'
        elif body == 'топ':
                link='https://pda.anekdot.ru/anekdots/top_day/'
        else:
                link='https://pda.anekdot.ru/anekdots/random/'
        try:
                data = read_url(link, UserAgents["Firefox"]).replace('<br>', '\n')
                data = re.findall(r'<div class="text">[^<]+', data)
                data = uHTML(data[0][18:])
                reply(mType, source, u"\n%s" % data)
        except:
                reply(mType, source, u"Ошибка")

def hahdler_poema(mType, source, body):
        try:
                data = read_url('https://pda.anekdot.ru/poems/random/', UserAgents["Firefox"]).replace('<br>', '\n')
                data = re.findall(r'<div class="text">[^<]+', data)
                data = uHTML(data[0][18:])
                reply(mType, source, u"\n%s" % data)
        except:
                reply(mType, source, u"Ошибка")

def hahdler_fraza(mType, source, body):
        try:
                data = read_url('https://pda.anekdot.ru/aphorisms/random/', UserAgents["Firefox"]).replace('<br>', '\n')
                data = re.findall(r'<div class="text">[^<]+', data)
                data = uHTML(data[0][18:])
                reply(mType, source, u"\n%s" % data)
        except:
                reply(mType, source, u"Ошибка")

def bashOrg(type, source, body):
        if body.isdigit():
                link = "http://bash.im/quote/%s" % body
        else:
                link = "http://bash.im/random"
        data = read_url(link, UserAgents["Firefox"])
        try:
                rate = re.search("data-vote-counter>(.+?)</div>", data, 16)
                id = re.search("data-quote=\"(.+?)\">", data, 16)
                data = re.search("<div class=\"quote__body\">(.+?)</div>", data, 16)
                rate = rate.group()[18:-6]
                id = id.group()[12:-2]
                data = data.group()[32:-6]
                if data:
                        answer = uHTML(u"\nЦитата: #%s Рейтинг: %s\n%s" % (id, rate, data))
                else:
                        answer = u"Ошибка."
                reply(type, source, answer)
        except Exception:
                reply(type, source, returnExc())


def itHappens(mType, source, body):
        try:
                if body and body.isdigit():
                        url = "http://ithappens.me/story/%s" % body
                else:
                        url = "http://ithappens.me/random"
                data = read_url(url, UserAgents["OperaMini"])
                data = re.search("<div class='text'>.*?</div>", data, 16)
                if data:
                        data = data.group()
                        data = stripTags(uHTML(data), " ")
                else:
                        data = u'Ошибка.'
                reply(mType, source, data)
        except Exception:
                reply(mType, source, returnExc())


## by Snapi-Snup autor
def bashAbyss(mType, source, args):
        try:
                rawhtml = read_url('http://bash.im/abysstop', UserAgents["BlackSmith"])
                elements = re.findall("<div class=\"quote__body\">(.+?)</div>", rawhtml, re.DOTALL)
                if elements:
                        rawquote = random.choice(elements)
                        message = "\n" + stripTags(uHTML(rawquote)[7:])
                else:
                        message = u"Что-то пусто..."
        except Exception:
                message = u"Что-то не так: %s" % str(returnExc())
        reply(mType, source, message)

def afor(type, source, body):
        try:
                data = re_search(read_url('http://skio.ru/quotes/humour_quotes.php',
                         UserAgents["Firefox"]), '<div class="qtext">', '<span class="qauthor"')
                data = stripTags(uHTML(data))
                reply(type, source, data)
        except Exception:
                reply(type, source, returnExc())

def getLinuxLink(mType, source, body):
        if not body:
                link = ""
                data = read_link("https://kernel.org")
                expression = re.search('<td id="latest_link">(.*?)</td>', data, 16)
                if expression:
                        link = expression.group(1)
                ver = getTagData("a", link)
                link = "https://kernel.org/%s" % getTagArg("a", "href", link).lstrip("./")
                reply(mType, source, u"Последняя стабильная версия ядра Linux: %(ver)s | %(link)s" % vars())

command_handler(bashOrg, 10, "quotes")
command_handler(itHappens, 10, "quotes")
command_handler(AnecDote, 10, "quotes")
command_handler(hahdler_poema, 10, "quotes")
command_handler(hahdler_fraza, 10, "quotes")
command_handler(bashAbyss, 10, "quotes")
command_handler(afor, 10, "quotes")
command_handler(getLinuxLink, 10, "quotes")