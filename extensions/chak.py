#===istalismanplugin===
# -*- coding: utf-8 -*-



def command_Chuck(mType, source, body):
        if body and check_number(body):
                Ask = "/quote/%d" % int(body)
        else:
                Ask = "/random"
        try:
                data = read_url("http://chucknorrisfacts.ru/%s" % Ask, UserAgents["BlackSmith"])
        except Exception as exc:
                answer = str(exc)
        except:
                answer = u"Не могу получить доступ к странице."
        else:
                pass
                comp = re.compile("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
                data = comp.search(data)
                if data:
                        answer = stripTags(uHTML(u"Факт #%s:\n%s" % data.groups()))
                else:
                        answer = u"Проблемы с разметкой..."
        reply(mType, source, answer)


register_command_handler(command_Chuck, 'чак', [], 10, 'Факты о Чаке Норрисе.', 'чак', ['чак'])