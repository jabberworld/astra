# BS mark.1
# /* coding: utf-8 */

#  BlackSmith plugin
#  vcard_plugin.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  Evgen [meb81@mail.ru]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_get_vcard(type, source, nick):
        if nick:
                if source[1] in GROUPCHATS:
                        if nick in GROUPCHATS[source[1]]:
                                if not GROUPCHATS[source[1]][nick]['ishere']:
                                        reply(type, source, u'его нет здесь')
                                        return
                                recipient = source[1]+'/'+nick
                        else:
                                recipient = nick
                else:
                        recipient = nick
        else:
                recipient = source[0]
        vcard_iq = xmpp.Iq(to = recipient, typ = 'get')
        INFA['outiq'] += 1
        vcard_iq.addChild('vCard', {}, [], 'vcard-temp')
        JCON.SendAndCallForResponse(vcard_iq, handler_vcard_answer, {'type': type, 'source': source, 'nick': nick})

def handler_vcard_answer(coze, stanza, type, source, nick):
                if stanza:
                        if stanza.getType() == 'result':
                                MASS = stanza.getChildren()
                                if MASS:
                                        repl, nickname, url, email, desc, bday, orgname, orgunit, title, gender, given, family, country, region, locality, street, number, name, to_repl = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', {'&lt;': '<', '&amp;': '&', '&quot;': '"', '&gt;': '>'}
                                        Props = MASS[0].getChildren()
                                        for Pr in Props:
                                                Pr_Name = Pr.getName()
                                                if Pr_Name == 'NICKNAME':
                                                        nickname = (Pr.getData()).strip()
                                                elif Pr_Name == 'FN':
                                                        name = (Pr.getData()).strip()
                                                elif Pr_Name == 'URL':
                                                        url = (Pr.getData()).strip()
                                                elif Pr_Name == 'EMAIL':
                                                        email = (Pr.getData()).strip()
                                                elif Pr_Name == 'DESC':
                                                        desc = (Pr.getData()).strip()
                                                elif Pr_Name == 'BDAY':
                                                        bday = (Pr.getData()).strip()
                                                elif Pr_Name == 'GENDER':
                                                        gender = (Pr.getData()).strip()
                                                elif Pr_Name == 'TITLE':
                                                        title = (Pr.getData()).strip()
                                        Query = unicode(stanza)
                                        if Query.count('<GIVEN>'):
                                                given = replace_all(((Query.replace('</GIVEN>', '<GIVEN>')).split('<GIVEN>')[1]), to_repl).strip()
                                        if Query.count('<FAMILY>'):
                                                family = replace_all(((Query.replace('</FAMILY>', '<FAMILY>')).split('<FAMILY>')[1]), to_repl).strip()
                                        if Query.count('<ADR>'):
                                                ADR = Query.split('<ADR>')
                                                if len(ADR) >= 2:
                                                        ADR = ADR[1]
                                                        if ADR.count('<COUNTRY>'):
                                                                country = replace_all(((ADR.replace('</COUNTRY>', '<COUNTRY>')).split('<COUNTRY>')[1]), to_repl).strip()
                                                        if ADR.count('<LOCALITY>'):
                                                                locality = replace_all(((ADR.replace('</LOCALITY>', '<LOCALITY>')).split('<LOCALITY>')[1]), to_repl).strip()
                                                        if ADR.count('<REGION>'):
                                                                region = replace_all(((ADR.replace('</REGION>', '<REGION>')).split('<REGION>')[1]), to_repl).strip()
                                                        if ADR.count('<STREET>'):
                                                                street = replace_all(((ADR.replace('</STREET>', '<STREET>')).split('<STREET>')[1]), to_repl).strip()
                                        if Query.count('<ORGNAME>'):
                                                orgname = replace_all(((Query.replace('</ORGNAME>', '<ORGNAME>')).split('<ORGNAME>')[1]), to_repl).strip()
                                        if Query.count('<ORGUNIT>'):
                                                orgunit = replace_all(((Query.replace('</ORGUNIT>', '<ORGUNIT>')).split('<ORGUNIT>')[1]), to_repl).strip()
                                        if Query.count('<TEL>'):
                                                tel = Query.split('<TEL>')
                                                for item in tel:
                                                        if item.count('</NUMBER><HOME /></TEL>'):
                                                                number = replace_all(((replace_all(item, {'<NUMBER>': '</NUMBER><HOME />', '</NUMBER><HOME /></TEL>': '</NUMBER><HOME />'})).split('</NUMBER><HOME />')[1]), to_repl).strip()
                                        if name in [family, given, '%s %s' % (given, family), '%s %s' % (family, given)]:
                                                name = ''
                                        if name:
                                                repl += u'\n~*~ Имя: '+name
                                        if nickname:
                                                repl += u'\n~*~ Псевдоним: '+nickname
                                        if given or family:
                                                repl += u'\n~*~ Полное имя: '+((given+' '+family).strip())
                                        if email:
                                                repl += u'\n~*~ Email: '+email
                                        if country:
                                                repl += u'\n~*~ Страна: '+country
                                        if region:
                                                repl += u'\n~*~ Регион: '+region
                                        if locality:
                                                repl += u'\n~*~ Город: '+locality
                                        if street:
                                                repl += u'\n~*~ Адрес: '+street
                                        if number:
                                                repl += u'\n~*~ Телефон: '+number
                                        if orgname:
                                                repl += u'\n~*~ Компания: '+orgname
                                        if orgunit:
                                                repl += u'\n~*~ Отдел: '+orgunit
                                        if title:
                                                repl += u'\n~*~ Должность: '+title
                                        if gender:
                                                gender = gender.lower()
                                                if gender == 'male':
                                                        repl += u'\n~*~ Пол: Мужской'
                                                if gender == 'female':
                                                        repl += u'\n~*~ Пол: Женский'
                                        if bday:
                                                repl += u'\n~*~ Днюха: '+bday
                                        if url:
                                                repl += u'\n~*~ Сайт: '+url
                                        if desc:
                                                repl += u'\n~*~ Инфа: '+desc
                                        if not repl:
                                                repl = u'Этот вкард было бы неплохо заполнить...'
                                        elif not nick:
                                                repl = u' Инфа о тебе:'+repl
                                        else:
                                                repl = (u'\nПро %s я знаю следующее:' % (nick))+repl
                                else:
                                        repl = u'Ничего не выходит... Косяк :('
                                reply(type, source, repl)

command_handler(handler_get_vcard, 10, "vcard")
