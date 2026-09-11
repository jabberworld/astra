#===istalismanplugin===
# -*- coding: utf-8 -*-
# Public Official Jabber-Quotes Plugin
# http://jabber-quotes.ru | http://jabber-net.ru

import urllib.request as urllib2
import urllib.parse

quote_api_key = '92aed58a4936317a594a7f386569dac9608d8f84559da13c79f768bb' # Сюда пишите ваш API-Ключ(если есть), который был получен при регистрации. -> http://jabber-quotes.ru/api .
# Без API-Ключа цитаты будут попадать на одобрение при добавлении, с api-ключем - сразу в базу.

quote_status = {'400 Bad Request': u'Неверный запрос.',
                '404 Not Found': u'Цитата не найдена.',
                '405 Method Not Allowed': u'Метод запроса не поддерживается.',
                '200 OK': u'Цитата успешно добавлена.',
                '204 Content Error': u'Превышение лимитов символов.',
                '400 Bad Reques': u'Неверный запрос.',
                '401 Unauthorized': u'API-Ключ введен неверено.',
                '423 Locked': u'Запрос заблокирован.',
                '500 Internal Server Error': u'Не удалось добавить цитату.'}

#######

def GetQuoteText(data):
    for node in data:
        if node.nodeType == node.TEXT_NODE:
            result = node.data
    return result

def ParseQuoteXML(data):
        import xml.dom.minidom
        xml = xml.dom.minidom.parseString(data)
        result = xml.getElementsByTagName('result')
        for x in result:
            if len(result[0].childNodes) == 7:
                quote = GetQuoteText(x.getElementsByTagName('quote')[0].childNodes)
                qid = GetQuoteText(x.getElementsByTagName('id')[0].childNodes)
                author = GetQuoteText(x.getElementsByTagName('author')[0].childNodes)
                result = u'Автор: %s\n%s\n---\nhttp://jabber-quotes.ru/id/%s' % (author,quote,qid)
            else:
                status = GetQuoteText(x.getElementsByTagName('status')[0].childNodes)
                result = u'%s' % (quote_status[status])
        return result

#######

def JabberQuotesRead(type,source,parameters):
        if parameters and parameters.isdecimal():
                url = 'http://jabber-quotes.ru/api/read/?id='+parameters
        else:
                url = 'http://jabber-quotes.ru/api/read/?id=random'
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Python-urllib/Official')
            opener = urllib2.build_opener()
            data = opener.open(req).read()
        except:
            reply(type,source,u'Не получилось подключится к серверу.')
            return 
        result = ParseQuoteXML(data)
        reply(type,source,result)

def JabberQuotesAdd(type,source,parameters):
    if parameters:
        if len(parameters)<=1500:
            values = {'quote' : parameters.encode('utf-8')}
            url = 'http://jabber-quotes.ru/api/add/'
            if quote_api_key:
                values['api'] = quote_api_key
            data = urllib.parse.urlencode(values)
            try:
                req = urllib2.Request(url, data)
                req.add_header('User-Agent', 'Python-urllib/Official')
                opener = urllib2.build_opener()
                data = opener.open(req).read()
            except:
                reply(type,source,u'Не получилось подключится к серверу.')
                return
            result = ParseQuoteXML(data)
            reply(type,source,result)
        else:
            reply(type,source,u'Лимит символов - 1500.')
    else:
        reply(type,source,u'Читай "помощь "!цитата+".')

register_command_handler(JabberQuotesRead, '!цитата', ['все'], 0, 'Показывает цитату с сайта jabber-цитатника http://jabber-quotes.ru\nБез параметров покажет случайную цитату.', '!цитата <id>', ['!цитата','!цитата 25'])
register_command_handler(JabberQuotesAdd, '!цитата+', ['все'], 16, 'Добавляет цитату на сайт jabber-цитатника http://jabber-quotes.ru\nПравила:\nМаксимальная длина цитаты - 1500 символов.\nПравила добавления цитаты - http://jabber-quotes.ru/api | http://jabber-quotes.ru/about', '!цитата+ <цитата>', ['!цитата+ <тест цитаты>'])
