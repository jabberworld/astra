#===istalismanplugin===
# -*- coding: utf-8 -*-

import time

chislo2568={}
chislo2569={}

def strateg(type, source, parameters):
        if not source[1] in GROUPCHATS:
                return
        if source[1] in chislo2568:
                reply(type,source, u'игра уже запущена')
                return
        groupchat = source[1]
        nick=source[2]
        jid=handler_jid(groupchat+'/'+nick)
        k = random.randrange(6, 25)
        if not jid in MONEY:
                 MONEY[jid] = 100
        e = u'Внимание! запускается игра "стратегия" я загадала число '+str(k)+u', если вы собираетесь играть, то в течение одной минуты напишите "в игре"'
        chislo2568[groupchat]={}
        chislo2568[groupchat]['1']={'strateg': k, 'time':time.time(), 'strateg2':1, 'strateg3':1, 'strateg4': k}
        chislo2568[groupchat][1]={'jid':jid, 'nick':nick}
        msg(groupchat, e)
        strateg_start569(type, source, k)
        strateg_start568(type, source, k)

def strateg_start568(type, source, k):
        groupchat = source[1]
        time.sleep(300)
        if groupchat in chislo2568:
                if chislo2568[groupchat]['1']['strateg']==k:
                        reply(type,source,u'5 минут истекли, игра автоматически завершается.')
                        del chislo2568[groupchat]

def strateg_start570(type, source, k):
        groupchat = source[1]
        time.sleep(60)
        if groupchat in chislo2569:
                if chislo2569[groupchat]['k']==k:
                        if groupchat in chislo2568:
                                reply(type,source,u'15 секунд истекли, ход переходит к другому')
                                chislo2568[groupchat]['1']['strateg2']+=1
                                del chislo2569[groupchat]
                                o=chislo2568[groupchat]['1']['strateg2']
                                if o in chislo2568[groupchat]:
                                        nick=chislo2568[groupchat][o]['nick']
                                        msg(groupchat, nick+u': Сейчас твой ход')

def strateg_start569(type, source, k):
        groupchat = source[1]
        time.sleep(60)
        if groupchat in chislo2568:
                if chislo2568[groupchat]['1']['strateg4']==k:
                        reply(type,source,u'Никто играть не захотел, смысла в игре нет, игра закончена')
                        del chislo2568[groupchat]
                        return
                if chislo2568[groupchat]['1']['strateg4']==0:
                        nick=chislo2568[groupchat][1]['nick']
                        msg(groupchat, nick+u': Сейчас твой ход')
                        chislo2569[groupchat]={}
                        k = random.randrange(0, 9999)
                        chislo2569[groupchat]={'k':k}
                        strateg_start570(type, source, k)
                
def strateg_msg(HREN,type,source,parameters):
        groupchat = source[1]
        nick=source[2]
        if groupchat not in GROUPCHATS:
                return
        jid=handler_jid(groupchat+'/'+nick)
        if not groupchat in chislo2568:
                return
        parameters=parameters.strip()
        if user_level(source,groupchat)>12:
                if parameters.lower()==u'стратегия стоп':
                        reply(type,source,u'игра прервана '+nick)
                        del chislo2568[groupchat]
                        return
        w = time.time()
        if w-chislo2568[groupchat]['1']['time']<60:
                if parameters.lower()==u'в игре':
                        if jid in chislo2568[groupchat]:
                                reply(type,source,u'ты уже есть в списке, ты че за двоих собрался играть?')
                        else:
                                reply(type,source,u'ваша заявка на игру принята')
                                chislo2568[groupchat]['1']['strateg3']+=1
                                ny=chislo2568[groupchat]['1']['strateg3']
                                chislo2568[groupchat]['1']['strateg4']=0
                                chislo2568[groupchat][ny]={'jid':jid, 'nick':nick}
                        return
                parameters23=parameters.isdigit()
                if parameters23 == False:
                        return
                reply(type,source,u'подожди 60 секунд, что так сложно что ли.')
        else:
                parameters23=parameters.isdigit()
                if parameters23 == False:
                        return
                if not chislo2568[groupchat]['1']['strateg2'] in chislo2568[groupchat]:
                        if chislo2568[groupchat]['1']['strateg2']>=chislo2568[groupchat]['1']['strateg3']:
                                chislo2568[groupchat]['1']['strateg2']=1
                        else:
                                chislo2568[groupchat]['1']['strateg2']+=1
                o=chislo2568[groupchat]['1']['strateg2']
                if chislo2568[groupchat][o]['jid']==jid:
                        parameters = int(parameters)
                        if parameters >3:
                                reply(type,source,u'вводи число 1,2 или 3')
                                return
                        t=chislo2568[groupchat]['1']['strateg']-parameters
                        if t==0:
                                if source[1] in TM.keys():
                                        TM[source[1]] += 50
                                        msg(source[1], u'+50 коинсов в копилку!\n\nВсего коинсов: '+str(TM[source[1]]))
                                if not jid in MONEY:
                                        MONEY[jid] = 100
                                MONEY[jid] += 15
                                with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
                                reply(type,source,u'ты выиграл, молодец\n Общий сщет: '+str(MONEY[jid])+'$')
                                del chislo2568[groupchat]
                                return
                        if t<0:
                                reply(type,source,u'ты проиграл и исключаешся из игры автоматически')
                                chislo2568[groupchat]['1']['strateg3']=chislo2568[groupchat]['1']['strateg3']-1
                                del chislo2568[groupchat][o]
                        else:
                                chislo2568[groupchat]['1']['strateg']=t
                        chislo2568[groupchat]['1']['strateg2']+=1
                        if not chislo2568[groupchat]['1']['strateg2'] in chislo2568[groupchat]:
                                if chislo2568[groupchat]['1']['strateg2']>=chislo2568[groupchat]['1']['strateg3']:
                                        chislo2568[groupchat]['1']['strateg2']=1
                                else:
                                        chislo2568[groupchat]['1']['strateg2']+=1
                        if groupchat in chislo2569:
                                del chislo2569[groupchat]
                        o=chislo2568[groupchat]['1']['strateg2']
                        if o in chislo2568[groupchat]:
                                nick=chislo2568[groupchat][o]['nick']
                                msg(groupchat, nick+u': Сейчас твой ход')
                        chislo2569[groupchat]={}
                        k = random.randrange(0, 9999)
                        chislo2569[groupchat]={'k':k}
                        strateg_start570(type, source, k)
                else:
                        reply(type,source,u'сейчас не твой ход, подождать своей очереди слабо?')

register_message_handler(strateg_msg)
register_command_handler(strateg, 'стратегия', ['все'], 10, 'Стартует игру с ботом', 'стратегия', ['стратегия'])