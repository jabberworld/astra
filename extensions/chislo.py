#===istalismanplugin===
# -*- coding: utf-8 -*-


chislo567 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
chislo2567={}

def chislo789(type, source, parameters):
 if not source[1] in GROUPCHATS:
  return
 if source[1] in chislo2567:
  reply(type,source, u'в данную игру уже играют, подождите 3 минуты.')
  return
 groupchat = source[1]
 nick=source[2]
 jid=handler_jid(groupchat+'/'+nick)
 if not jid in MONEY:
  MONEY[jid] = 100
  with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
 e = u'я загадала число от 0 до 10, ставка 5$, попробуйте его отгадать у вас есть 3 попытки. Также это необходимо сделать за 3 минуты. Поехали!\nОбщий счет: '+str(MONEY[jid])+'$'
 k = random.randrange(0, 9999)
 hh = random.choice(chislo567)
 chislo2567[groupchat]={}
 chislo2567[groupchat][jid]={'chislo':hh, 'chislo1': 0, 'chislo2': k}
 reply(type,source, e)
 chislo_start567(type, source, jid, k)

def chislo_start567(type, source, jid, k):
 groupchat = source[1]
 nick=source[2]
 time.sleep(180)
 if groupchat in chislo2567:
  if jid in chislo2567[groupchat] and nick in GROUPCHATS[groupchat] and chislo2567[groupchat][jid]['chislo2'] == k:
   reply(type,source,u'3 минуты истекли, игра закончена.')
   del chislo2567[groupchat]

def chislo_msg(raw,type,source,parameters):
 groupchat = source[1]
 nick=source[2]
 if groupchat not in GROUPCHATS:
  return
 jid=handler_jid(groupchat+'/'+nick)
 if not groupchat in chislo2567:
  return
 if jid in chislo2567[groupchat]:
  parameters=parameters.strip()
  parameters23=parameters.isdigit()
  if parameters23 == False:
   return
  parameters = int(parameters)
  if parameters<0 or parameters>10:
   reply(type,source,u'число должно быть от 0 до 10')
   return
  chislo2567[groupchat][jid]['chislo1']+=1
  if parameters == chislo2567[groupchat][jid]['chislo']:
   MONEY[jid] += 25
   reply(type,source,u'поздравляю вы угадали число!\n Общий счет: '+str(MONEY[jid])+'$' )
   confa = source[1]
   if confa in TM.keys():
    TM[confa] += 50
    msg(confa, u'+50 коинсов в копилку!\n\n\nВсего Коинсов: '+str(TM[confa]))
   with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
   del chislo2567[groupchat]
   return
  else:
   if parameters > chislo2567[groupchat][jid]['chislo']:
    if chislo2567[groupchat][jid]['chislo1'] == 3:
     e = chislo2567[groupchat][jid]['chislo']
     MONEY[jid] -= 5
     reply(type,source,u'вы проиграли, я загадала число '+unicode(e)+u'\nОбщий счет: '+str(MONEY[jid])+'$' )
     with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
     del chislo2567[groupchat]
     return
    reply(type,source,u'истинное число меньше вашего')
    return
   if parameters < chislo2567[groupchat][jid]['chislo']:
    if chislo2567[groupchat][jid]['chislo1'] == 3:
     e = chislo2567[groupchat][jid]['chislo']
     MONEY[jid] -= 5
     with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
     reply(type,source,u'вы проиграли, я загадала число '+unicode(e)+u'\nОбщий счет: '+str(MONEY[jid])+'$' )
     del chislo2567[groupchat]
     return
    reply(type,source,u'истинное число больше вашего')
    return

register_message_handler(chislo_msg)
register_command_handler(chislo789, 'число', ['мук','все'], 10, 'Стартует игру с ботом, Бот загадывает число от 0 до 10 и вам необходимо его отгадать', 'число', ['число'])
