# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1

#  Author: SaranskCity

def handler_joke1(type, source, nick):
        if type == 'public':
                nicks = []
                buhlo = [u'водки', u'самогона', u'пива', u'коньячка', u'абсента', u'вина', u'чачи', u'виски', u'боярышника на спирту', u'текилы', u'бурбона', u'мордовской фирменной настоечки по дедовскому методу']
                msg(source[1], '/me сегодня за бармена')
                for n in list(GROUPCHATS[source[1]]):
                        if GROUPCHATS[source[1]][n]['ishere']:
                                nicks.append(n)
                rnd_nick = random.choice(nicks)
                for i in nicks:
                        if i != rnd_nick:
                                msg(source[1], u'/me налила %s %s грамм %s' % (i, random.randrange(10, 50) * 10, random.choice(buhlo)))
                                time.sleep(0.9)
                time.sleep(25)
                msg(source[1], u'а %s не налила, он(а) уже и так блюёт' % rnd_nick)
        else:
                reply(type, source, u'только в чате!')

def handler_joke2(type, source, nick):
        if type == 'public':
                nicks = []
                food = [u'наваристой шурпы', u'картофель в томатном соусе с фрикадельками', u'лагман узбекский', u'суп из белых грибов с фрикадельками', u'суп из форели с помидорами и чили', u'суп с креветками', u'суп харчо', u'окрошку на сметане', u'котлетки c пюрешкой', u'сельдь под шубой', u'макароны по флодски', u'мясо по-французски с картофелем и помидорами', u'блинчики да не простые, а с начинокой - красной икрой', u'пироги с капустой', u'телятину «Орлов»', u'рулет из свинины', u'гречку с бараниной', u'мясо с овощами в духовке', u'бефстроганов']
                base = [u'подала', u'принёсла', u'притащила', u'приготовила для', u'заварганила', u'подала на стол']
                msg(source[1], '/me сегодня за повара')
                for n in list(GROUPCHATS[source[1]]):
                        if GROUPCHATS[source[1]][n]['ishere']:
                                nicks.append(n)
                rnd_nick = random.choice(nicks)
                for i in nicks:
                        if i != rnd_nick:
                                msg(source[1], u'/me %s %s %s' % (random.choice(base), i, random.choice(food)))
                                time.sleep(0.9)
                time.sleep(25)
                msg(source[1], u'а %s не дала, он(а) уже и так объелся!' % rnd_nick)
        else:
                reply(type, source, u'только в чате!')

def handler_oboobs(type, source, nick):
        if type == 'public':
                if nick:
                        if nick != handler_botnick(source[1]):
                                if nick in GROUPCHATS[source[1]]:
                                        data = read_url('http://api.oboobs.ru/noise/1/', UserAgents["Firefox"])
                                        try:
                                                reply(type, source, u'Вот похоже сиськи %s - http://media.oboobs.ru/%s' % (nick, simplejson.loads(data)[0]['preview'].replace('_preview', '')))
                                        except:
                                                reply(type, source, u'Ошибка загрузки сисек с сервера')
                                else:
                                        reply(type, source, u'я тут таких не вижу или это не сисястый чел')
                        else:
                                reply(type, source, u'у меня нет сисек :)')
                else:
                        reply(type, source, u'тебе чьи сиськи то показать?!')
        else:
                reply(type, source, u'только в конференции')
                
def handler_obutts(type, source, nick):
        if type == 'public':
                if nick:
                        if nick != handler_botnick(source[1]):
                                if nick in GROUPCHATS[source[1]]:
                                        data = read_url('http://api.obutts.ru/noise/1/', UserAgents["Firefox"])
                                        try:
                                                reply(type, source, u'Вот похожая попка %s - http://media.obutts.ru/%s' % (nick, simplejson.loads(data)[0]['preview'].replace('_preview', '')))
                                        except:
                                                reply(type, source, u'Ошибка загрузки жопеней с сервера')
                                else:
                                        reply(type, source, u'я тут таких не вижу или эта жопа не поместилась на экран')
                        else:
                                reply(type, source, u'у меня нет жопы :)')
                else:
                        reply(type, source, u'чьи попки смотреть то будем?')
        else:
                reply(type, source, u'только в конференции')

command_handler(handler_joke1, 10, "joke")
command_handler(handler_joke2, 10, "joke")
command_handler(handler_oboobs, 10, "joke")
command_handler(handler_obutts, 10, "joke")
