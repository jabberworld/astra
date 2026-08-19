#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

SEA_BAT='dynamic/sea_bat.txt'

SBT={}

SBT_FIELD=""".   a  b  c  d  e  f  g
1 |  |  |  |  |  |  |  |
2 |  |  |  |  |  |  |  |
3 |  |  |  |  |  |  |  |
4 |  |  |  |  |  |  |  |
5 |  |  |  |  |  |  |  |
6 |  |  |  |  |  |  |  |"""

def sea_bat_start(type, source, parameters):
        if not source[1] in GROUPCHATS.keys():
                return
        if parameters==u'топ':
                sea_bat_get(type, source, parameters)
                return
        if type!='private':
                reply(type, source, u'Начать игру можно только через приват бота!')
                return
        if len(SBT)>20:
                reply(type, source, u'На данный момент в игре больше 20-ти человек!Попробуйте позже!')
                return
        jid=handler_jid(source[1]+'/'+source[2])
        if jid in SBT.keys():
                if SBT[jid]['with']:
                        for x in SBT.keys():
                                if x==SBT[jid]['with']:
                                        msg(SBT[x]['source'], unicode(SBT[jid]['nick'])+u' вышел, игра окончена!')
                                        del SBT[x]
                del SBT[jid]
                reply(type, source, u'Вы выйшли из игры!')
                return
        SBT[jid]={'id':random.randrange(10,40), 'h':0, 'source':source[1]+'/'+source[2],'nick':source[2], 'die':[], 'map':'', 'kill':0, 'with':'', 'field':{}, 'time':time.time(), 'miss':[]}
        if not SBT:
                reply(type, source, u'На данный момент в игре никого нет!')
                return
        nick=''
        for x in SBT:
                if x!=jid and not SBT[x]['with']:
                        nick=SBT[x]['nick']
                        SBT[x]['with']=jid
                        SBT[jid]['with']=x
                        msg(SBT[x]['source'], u'Вы играете с '+unicode(SBT[jid]['nick'])+u'!\n'+SBT_FIELD+u'\nУ вас есть четыре корабля, заполните поле отправив расположение кораблей через кому, напр. a2,g3,b6,b2')
                        break
        if not nick and not SBT[jid]['with']:
                reply(type, source, u'На данный момент нет свободных игроков!\nВы можете подождать пока кто-то зайдет, либо выйти (повторно мор_бой)')
                return
        reply(type, source, u'Вы играете с '+nick+u'!\n'+SBT_FIELD+u'\nУ вас есть четыре корабля, заполните поле отправив расположение кораблей через кому, напр. a2,g3,b6,b2')

def seabatl_msg(raw, type, source, parameters):
        C={'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7}
        B={'a':0, 'b':6, 'c':12, 'd':18, 'e':24, 'f':30, 'g':36}
        if not source[1] in GROUPCHATS.keys():
                return
        if parameters.lower() in COMMANDS.keys():
                return
        jid=handler_jid(source[1]+'/'+source[2])
        a=parameters.strip()
        n=''
        if jid in SBT.keys() and type=='private':
                if SBT[jid]['with']:
                        if not SBT[jid]['field']:
                                if parameters.count(',')==3:
                                        if not a.count(' '):
                                                d=parameters.split(',')
                                                for x in d:
                                                        if len(x)!=2:
                                                                reply(type, source, x+u' - недопустимое значение!')
                                                                return
                                                        if not x[:1] in C.keys() or not x[-1:].isdigit():
                                                                reply(type, source, x+u' - недопустимое значение!')
                                                                return
                                                        n=B[x[:1]]+int(x[-1:])
                                                        SBT[jid]['field'][n]={}
                                                reply(type, source, u'Ваша карта:\n'+sbt_view(0, jid))
                                                n=u'Первым ходите вы!'
                                                if SBT[SBT[jid]['with']]['field']:
                                                        if SBT[SBT[jid]['with']]['id']>SBT[jid]['id']:
                                                                n=u'Первый ход - ход вашего соперника!'
                                                                SBT[SBT[jid]['with']]['h']=1
                                                                msg(SBT[SBT[jid]['with']]['source'],u'Игра началась!\nПервым ходите вы!')
                                                        else:
                                                                SBT[jid]['h']=1
                                                                msg(SBT[SBT[jid]['with']]['source'],u'Игра началась!\nПервый ход - ход вашего соперника!')
                                                        reply(type, source, u'Игра началась!\n'+n)
                                                        return
                                                reply(type, source, u'Ждем пока ваш противник заполнит поле!')
                                        else:
                                                reply(type, source, u'Пиши без пробелов!')
                                else:
                                        reply(type, source, u'Что-то сделано не верно!')
                        else:
                                if len(parameters)==2:
                                        if parameters[:1] in C.keys() and parameters[-1:].isdigit():
                                                n=B[parameters[:1]]+int(parameters[-1:])
                                                if not SBT[jid]['h']:
                                                        reply(type, source, u'Сейчас ходит ваш соперник!')
                                                        return
                                                if n in SBT[SBT[jid]['with']]['field']:
                                                        if n in SBT[SBT[jid]['with']]['die'] or n in SBT[SBT[jid]['with']]['miss']:
                                                                reply(type, source, u'Сюда вы уже стреляли! Выберите другие координаты!')
                                                                return
                                                        SBT[jid]['h']=0
                                                        SBT[SBT[jid]['with']]['die'].append(n)
                                                        for x in SBT:
                                                                if SBT[x]['with']==jid:
                                                                        reply(type, source, u'Убит!\nКарта вашего соперника:\n'+sbt_view(1, x))
                                                                        msg(SBT[x]['source'],parameters+u' убит!\n'+sbt_view(1, x))
                                                                        if SBT[x]['kill']==3:
                                                                                reply(type, source, u'Вы выиграли!\nВаша карта\n'+sbt_view(0,jid)+u'\nКарта соперника\n'+sbt_view(0,x))
                                                                                msg(SBT[x]['source'],u'Вы проиграли!\nВаша карта\n'+sbt_view(1,x)+u'\nКарта соперника\n'+sbt_view(0,jid))
                                                                                del SBT[jid]
                                                                                del SBT[x]
                                                                                try:
                                                                                        if not os.path.exists(SEA_BAT):
                                                                                                fp=open(SEA_BAT, 'w')
                                                                                                fp.write('{}')
                                                                                                fp.close()
                                                                                        txt=eval(read_file(SEA_BAT))
                                                                                        if not jid in txt:
                                                                                                txt[jid]={}
                                                                                                txt[jid]={'n':1}
                                                                                                write_file(SEA_BAT, str(txt))
                                                                                        else:
                                                                                                txt[jid]['n']+=1
                                                                                                write_file(SEA_BAT, str(txt))
                                                                                except:
                                                                                        pass
                                                                                break
                                                                        SBT[jid]['h']=1
                                                                        reply(type, source, u'Ваш ход!')
                                                                        SBT[x]['kill']+=1
                                                                        return
                                                else:
                                                        SBT[jid]['h']=0
                                                        for x in SBT:
                                                                if SBT[x]['with']==jid:
                                                                        SBT[x]['miss'].append(n)
                                                                        reply(type, source, u'Мимо!\nКарта вашего соперника:\n'+sbt_view(1, x))
                                                                        msg(SBT[x]['source'], parameters+u' мимо!')
                                                                        break
                                                        msg(SBT[SBT[jid]['with']]['source'],u'Ваш ход!')
                                                        SBT[SBT[jid]['with']]['h']=1
                                                        
                                
def sbt_view(public, jid):
        if not jid in SBT:
                return None
        SBT_REP=""".   a  b  c  d  e  f  g
%s |01|07|13|19|25|31|37|
%s |02|08|14|20|26|32|38|
%s |03|09|15|21|27|33|39|
%s |04|10|16|22|28|34|40|
%s |05|11|17|23|29|35|41|
%s |06|12|18|24|30|36|42|""" % ('one','two','three','four','five','six')
        k='  '
        for x in SBT[jid]['field']:
                k='  '
                if x in SBT[jid]['die']:
                        k='X'
                else:
                        if not public:
                                k='*'
                x=str(x)
                if len(x)==1:
                        x='0'+x
                SBT_REP=SBT_REP.replace(str(x),k)
        for m in SBT[jid]['miss']:
                m=str(m)
                if len(m)==1:
                        m='0'+m
                SBT_REP=SBT_REP.replace(str(m),' .')
        for c in SBT_REP:
                if c.isdigit():
                        SBT_REP=SBT_REP.replace(c,' ')
        return SBT_REP.replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6')

def sea_bat_leave(groupchat, nick, n, nm):
        jid=handler_jid(groupchat+'/'+nick)
        if not SBT:
                return
        if jid in SBT.keys():
                if not SBT[jid]['with']:
                        return
                for x in SBT.keys():
                        if x==SBT[jid]['with']:
                                msg(SBT[x]['source'], unicode(SBT[jid]['nick'])+u' вышел, игра окончена!')
                del SBT[SBT[jid]['with']]
                del SBT[jid]

def sea_bat_get(type, source, parameters):
        if not os.path.exists(SEA_BAT):
                fp=open(SEA_BAT, 'w')
                fp.write('{}')
                fp.close()
        try:
                txt=eval(read_file(SEA_BAT))
                if not txt:
                        reply(type, source, u'Статистики нет!')
                        return
                rep=''
                for x in txt:
                        rep+=x.split('@')[0]+' - '+str(txt[x]['n'])+'\n'
                JCON.send(xmpp.Message(source[1]+'/'+source[2],rep[:5000],'chat'))
        except:
                reply(type, source, u'ошибка в базе')

register_message_handler(seabatl_msg)                
register_leave_handler(sea_bat_leave)               
register_command_handler(sea_bat_start, 'мор_бой', ['мафия','все'], 10, 'Морской бой (beta). Для статистики наберите мор_бой топ', 'мор_бой', ['мор_бой'])



