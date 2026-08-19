# BS mark.1-55
# /* coding: utf-8 */

def handler_holidays(type, source, body):
        try:
                data = read_url('http://www.calend.ru/img/export/calend.rss', 'Mozilla/5.0')
                pass
                data = data.replace('\n', ' ')
                data = re.search(r'<item>.*', data)
                text = ''
                if data:
                        data = data.group()
                        for i in re.findall(r'<title>[^<]+<\/title>', data):
                                text = text + '\n' + i[7:-8]
                else:
                        text = u'Ошибка обработки данных'
                reply(type, source, text)
        except:
                reply(type, source, u'По вашему запросу ничего не найдено')

command_handler(handler_holidays, 10, "holydays")
