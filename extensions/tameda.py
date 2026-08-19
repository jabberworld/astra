#===istalismanplugin===
# -*- coding: utf-8 -*-

A_C_T = {}
TE = {}
TW = {}
TENE = {}
TD = {}
TT = {}
TI = {}
TG = {}
TM = {}
TALK = {}
TL = {}

def live_t(t,s,p):
   c = s[1]
   if c in A_C_T.keys():
      if TL[c] < 100:
         if p == u'витаминку':
            TL[c] += 5
            reply(t,s,u'Фу бяка....лучше б ты мне леденцов на палочке дал...')
            msg(c,u'+5 здоровья')
            return
         else:
            reply(t,s,u'Не хочу...')
            return
      else:
         reply(t,s,u'Со мной все в порядке')
         return
   else:
      reply(t,s,u'Тамагочи выключен')

register_command_handler(live_t, 'выпей', [], 10, 'Повышает здоровье бота', 'выпей витаминку', ['выпей витаминку'])

def t_son(type, source, parameters):
   confa = source[1]
   if parameters == u'спать':
      if confa in A_C_T.keys():
         if TENE[confa] < 150:
            TENE[confa] += 900
            handler_set_prefix(type,source,'*')
            msg(source[1],u'/me пошла спатки.....')
            status='away'
            change_bot_status(source[1],u'Сплю *LAZY*',status)
            time.sleep(10000)
            if source[1] in PREFIX:
               del PREFIX[source[1]]
               write_file('dynamic/%s/prefix.txt' % (source[1]), "'none'")
               reply(type,source,u'Ооооох выспалаааась......')
               message = STATUS[source[1]]['message']
               status = STATUS[source[1]]['status']
               change_bot_status(source[1], message, status)
            else:
               return
         else:
            reply(type, source, u'Я пока не хочу спать.....')
      else:
         reply(type, source, u'Тамагочик Выключен')
   else:
      return

register_command_handler(t_son, 'пойди', [], 10, 'Отправляет бота в сон', 'пойди спать', ['пойди спать'])

def handler_govori(type,source,parameters):
   confa = source[1]
   if parameters == '1':
      if confa in A_C_T.keys():
         reply(type, source, u'Уже включено.')
         return
      A_C_T[confa] = 1
      fp = file('dynamic/tamcont.txt', 'w')
      fp.write( str(A_C_T) )
      fp.close()
      msg(source[1], u'Привет! Меня зовут Астра. Я тамагочи. Давайте знакомиться :) \n\nНапишите:\nимя Ваше_имя\n\nЧто бы я знала как к Вам обратиться')
      TENE[confa] = 500
      TD[confa] = 200
      TW[confa] = 150
      TE[confa] = 100
      TG[confa] = 300
      TALK[confa] = 300
      TL[confa] = 100
      if confa not in TT.keys():
         TT[confa] = 0
         TI[confa] = 0
         TM[confa] = 1000
      while A_C_T[confa]:
         time.sleep(240)
         TW[confa] -= 1
         TD[confa] -= 1
         TE[confa] -= 1
         TENE[confa] -= 1
         TG[confa] -= 1
         TT[confa] += 4
         TALK[confa] -= 0.5
         tt_save_now()
         tm_save_now()
         TI[confa] += 0.01
         intelekt_save_now()
         if TE[confa] <= 5:
            mis = [u' А что там в холодильнике есть? Я что-то проголодалась....',u'А что тама в холодильнике?',u'Кушать хочеться',u'Мяу мяу накорми меняу']
            mes = random.choice(mis)
            msg(source[1],mes)
            if TE[confa] <= 0:
               if TM[confa] > 50:
                  TE[confa] += 250
                  TM[confa] -= 50
                  msg(source[1],u'пойду по зырю че там в холодильнике, вас пока дождешься....')
               else:
                  TL[confa] -= 1
         elif TW[confa] <= 5:
            mis1 = [u'Пить охото',u'Хачу кофе',u'Газировки хочется',u'Мяу мяу напои меняу']
            mes1 = random.choice(mis1)
            msg(source[1],mes1)
            if TW[confa] <= 0:
               if TM[confa] > 50:
                  TW[confa] += 250
                  TM[confa] -= 50
                  msg(source[1],u'пойду по зырю че там в холодильнике, вас пока дождешься....')
               else:
                  TL[confa] -=1
         elif TENE[confa] <= 5:
            mis3 = [u'Спатки хочется.....',u'Спать охото....',u'щас мну вырубит']
            mes3 = random.choice(mis3)
            msg(source[1],mes3)
            if TENE[confa] <= 0:
               TENE[confa] += 500
               msg(source[1],u'пойду приму допинг....')
         elif TD[confa] <= 5:
            mis4 = [u'Никто меня не замечает ((((( Поиграйте со мной ((((',u'Играть хочу....',u'Хде мой мячик?',u'Мяу мяу поиграй со мной']
            mes4 = random.choice(mis4)
            msg(source[1],mes4)
            if TD[confa] <= 0:
               TD[confa] += 50
               msg(source[1],u'/me гоняется за заводной мышкой......')
         elif TG[confa] <= 5:
            mis5 = [u'Лоток грязный', u'Хачу расческу', u'Колтуны замучали', u'Хде мой шампунь', u'Эх...опять в воду лезть надо фууууу', u'Шо так воняет....']
            mes5 = random.choice(mis5)
            msg(source[1], mes5)
            if TG[confa] <= 0:
               TG[confa] += 300
               msg(source[1],u'/me пошла прогулятся....заодно кустики поищу....')
         elif TL[confa] <= 0:
            msg(confa, u'Смерть тамагочика....')
            del TM[confa]
            del TT[confa]
            del TI[confa]
            del A_C_T[confa]
   elif parameters == '0':
      if confa in A_C_T.keys():
         intelekt_save_now()
         tt_save_now()
         del A_C_T[confa]
         del TENE[confa]
         fp = file('dynamic/tamcont.txt', 'w')
         fp.write( str(A_C_T) )
         fp.close()
         reply(type, source, u'Выключено')
      else:
         reply(type, source, u'И так выключено')
   else:
      if confa in A_C_T.keys():
         reply(type, source, u'Включено')
      else:
         reply(type, source, u'Выключено')

register_command_handler(handler_govori, 'тамагочи', [], 20, 'Тамагочик', 'тамагочи 1', ['тамагочи 0'])


   


def tamagochi_load_now(conf):
   global A_C_T
   try:
      fp = file('dynamic/tamcont.txt', 'r')
      A_C_T = eval( fp.read() )
      fp.close()
      if conf in A_C_T.keys():
         handler_govori()
   except:
      fp = file('dynamic/tamcont.txt', 'w')
      A_C_T = {}
      fp.write( str(A_C_T) )
      fp.close()

register_stage1_init(tamagochi_load_now)

def t_gigiena(type, source, parameters):
   confa = source[1]
   if parameters == u'горшок':
      if confa in A_C_T.keys():
         if TI[confa] >= 0:
            if TG[confa] <= 900:
               reply(type, source, u'Неужели, решили в кои то веки мой горшок убрать....')
               TG[confa] += 300
               return
            else:
               reply(type, source, u'Не хачу')
               return
         else:
            reply(type, source, u'Недостаточно интеллекта')
            return
      else:
         reply(type, source, u'Тамагочик не запущен.')
         return
   elif parameters == u'расческа':
      if confa in A_C_T.keys():
         if TI[confa] >= 5.00:
            if TG[confa] <= 900:
               reply(type, source, u'Вуаля... Спасибо заботливый человечег :)')
               TG[confa] += 300
               return
            else:
               reply(type, source, u'Не хачу')
               return
         else:
            reply(type, source, u'Недостаточно интеллекта')
            return
      else:
         reply(type, source, u'Тамагочик незапущен.')
         return
   if parameters == u'ванна':
      if confa in A_C_T.keys():
         if TI[confa] >= 10.00:
            if TG[confa] <= 900:
               reply(type, source, u'Фу гадкая вода..... Эй, тихо ты, шампунь в глаза лезет')
               TG[confa] += 300
               return
            else:
               reply(type, source, u'Не хачу')
               return
         else:
            reply(type, source, u'Недостаточно интеллекта')
            return
      else:
         reply(type, source, u'Тамагочик не запущен')
         return
   else:
      reply(type, source, u'Повышает гигиену тамагочика. Доступные параметры: горшок, расческа, ванна')

register_command_handler(t_gigiena, 'гигиена', [], 10, 'Следит за чистотой. Доступные параметры: горшок, расческа, ванна.', 'гигиена горшок', ['гигиена ванна'])

def t_sost(type,source, body):
   confa = source[1]
   if confa in A_C_T.keys():
      confa = source[1]
      reply(type, source, u'Мое состояние:\n*<>*<>*<>*<>*<>*<>*\n > Голод: '+str(TE[confa])+u' <\n > Жажда: '+str(TW[confa])+u' <\n > Энергия: '+str(TENE[confa])+u' <\n > Отдых: '+str(TD[confa])+u' <\n > Гигиена: '+str(TG[confa])+u' <\n > Здоровье: '+str(TL[confa])+u' <\n > Возраст: '+str(TT[confa])+u' мин. <\n > Интеллект: '+str(TI[confa])+u' <\n > Коинсы: '+str(TM[confa])+' <\n*<>*<>*<>*<>*<>*<>*')
   else:
      reply(type, source, u'Тамагочи выключем.')
      
register_command_handler(t_sost, 'состояние', [], 10, 'Показывает состояние тамогочи.', 'состояние', ['состояние'])

def t_read(type, source, parameters):
   confa = source[1]
   if parameters == u'букварь':
      if confa in A_C_T.keys():
         if TI[confa] >= 3.00:
            reply(type, source, u'Урра! Мы будем учить буквы!')
            TI[confa] += 0.03
            TG[confa] -= 5
            intelekt_save_now()
         else:
            reply(type, source, u'Я узнаю что это когда уровень интелекта станет 3 уровня.')
            return
      else:
         reply(type, source, u'Тамагочик выключен.')
         return
   if parameters == u'Сказки':
      if confa in A_C_T.keys():
         if TI[confa] >= 10.00:
            reply(type, source, u'Урра! Мы будем читать сказки :)')
            TI[confa] += 0.05
            TG[confa] -= 5
            intelekt_save_now()
         else:
            reply(type, source, u'Я узнаю что это когда уровень интелекта станет 10 уровня.')
            return
      else:
         reply(type, source, u'Тамагочик выключен.')
         return
   if parameters == u'книгу':
      if confa in A_C_T.keys():
         if TI[confa] >= 20.00:
            reply(type, source, u'Пойду почитаю немного')
            TI[confa] += 0.07
            TG[confa] -= 5
            intelekt_save_now()
         else:
            reply(type, source, u'Я узнаю что это когда уровень интелекта станет 20 уровня.')
            return
      else:
         reply(type, source, u'Тамагочик выключен.')
         return
   else:
      reply(type, source, u'Повышает интеллект тамагочика. Доступные параметры: букварь, книгу, сказки.')

register_command_handler(t_read, 'почитай', [], 10, 'Доступные параметры: букварь, сказки, книгу', 'почитай букварь', ['почитай книгу'])

def handler_tam_eda(type,source,parameters):
    confa = source[1]
    if confa in A_C_T.keys():
        if type == 'private':
            reply(type,source,u'только для чата :)')
            return
        if parameters==u'кашу':
            TG[confa] -= 5
            if TM[confa] <=14:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 15
            reply(type,source,u'а не буду я твою кашу *NO*')
            time.sleep(10)
            reply(type,source,u'или давай банан, или отстань')
        if parameters==u'банан':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 14:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TE[confa] += 40
            TG[confa] -= 5
            TM[confa] -= 15
            mis = [u'спасибо ;)',u'опа бананы.....',u'чафк....чавк.....цацк...чафк']
            mes = random.choice(mis)
            reply(type,source,mes)
            time.sleep(120)
            mis2 = [u'еще хочу :)',u'а добавка? :)',u'а у нас че только бананы?',u'че еще там в холодильнике?']
            mes2=random.choice(mis2)
            msg(source[1],mes2)
        if parameters==u'макароны':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 49:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TE[confa] += 200
            TG[confa] -= 5
            TM[confa] -= 50
            mis1 = [u'как проголодаюсь сообщу :)',u'няма няма :)',u'а часиков через пять супчик будет?']
            mes1 = random.choice(mis1)
            reply(type,source,mes1)
            time.sleep(300)
            reply(type,source,u'спасибо :)')
        if parameters==u'супчик':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 49:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TE[confa] += 200
            TG[confa] -= 5
            TM[confa] -= 50
            reply(type,source,u'это дело я люблю.....')
            time.sleep(620)
            reply(type,source,u'Ох...наелась, как проголодаюсь сообщу')
        if parameters==u'клубнику':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 19:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TE[confa] += 50
            TG[confa] -= 5
            TM[confa] -= 20
            reply(type,source,u'О... Клубника....пойду за сливками схожу.....')
            time.sleep(500)
            reply(type,source,u'хороша клубника :)')
        if parameters==u'чипсы':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 24:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 25
            TE[confa] += 50
            TG[confa] -= 5
            reply(type,source,u'хрум фрум хрум фрум')
            time.sleep(600)
            reply(type,source,u'че тама кусное есть?')
        if parameters==u'винегрет':
            if TE[confa] > 500:
                reply(type,source, u'Не хочется *NO*')
                return
            if TM[confa] <= 29:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TE[confa] += 40
            TG[confa] -= 5
            TM[confa] -= 30
            reply(type,source,u'буду винегрет запивать водкой....  :-!  Водка выходит легко, а винегрет красиво....')
            time.sleep(15)
            reply(type,source,u'ну и гадость ваша заливная рыба...а можно мне ещё?')
        if parameters==u'вискас':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 29:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 40
            TE[confa] += 150
            TG[confa] -= 5
            reply(type,source,u'Ура!!! Мяу мясо!!! *AAA*')
            time.sleep(60)
            reply(type,source,u'мур мур муррр-р *CAT*')
        if not parameters:
            reply(type,source,u'ну и че я буду кушать? Дай мне лучше кашу или банан')
        if parameters==u'торт':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 29:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 30
            TE[confa] += 80
            TG[confa] -= 5
            reply(type,source,random.choice([u'Тортик...ням ням...',u'ух ты какая вкусняшка',u'ну ты и остальным торт тоже раздай, все вместе захаваем']))
            time.sleep(300)
            reply(type,source,u'пасибо :)')
        if parameters==u'бутерброд':
            confa = source[1]
            if TE[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 19:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 20
            TE[confa] += 70
            TG[confa] -= 5
            reply(type,source,random.choice([u'че в сухомятку? Тогда и кофе давай',u'а бутерброд с колбасой или с маслом?',u'пасибо :) а я тут как раз думала че бы перекусить']))
            time.sleep(290)
            reply(type,source,random.choice([u'спасибо :)',u'перекусила :)',u'хоть бутербродом перекусила :) а то обычно приходится провода перекусывать']))
    else:
        reply(type, source, u'Тамагочи выключен.')

def handler_tam_pit(type,source,parameters):
    confa = source[1]
    if confa in A_C_T.keys():
        if type=='private':
            reply(type,source,u'пиши в чате')
            return
        if parameters==u'минералку':
            confa = source[1]
            if TW[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 39:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 40
            TW[confa] += 150
            TG[confa] -= 5
            reply(type,source,u'как раз пить охото :)')
        if parameters==u'вино':
            confa = source[1]
            if TW[confa] > 900:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 59:
                reply(type,source, u'Недостаточно Коинсов')
                return
            if TALK[confa] > 300:
                reply(type,source,u'Куда столько бухать?!')
                return
            TM[confa] -= 60
            TW[confa] += 300
            TG[confa] -= 5
            TALK[confa] += 300
            mis3=[u'ты че упал что ли???',u'я ж напьюсь...',u'щас напьюсь и буду буянить',u'ты меня че споить решил?']
            mes3=random.choice(mis3)
            reply(type,source,mes3)
            time.sleep(600)
            reply(type,source,u'кажиись яа напийлась *ALCOHOLIC*')
        if parameters==u'водку':
            confa = source[1]
            if TW[confa] > 900:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 39:
                reply(type,source, u'Недостаточно Коинсов')
                return
            if TALK[confa] > 300:
                reply(type,source,u'Куда столько бухать?!')
                return
            TALK[confa] += 300
            TM[confa] -= 40
            TW[confa] += 300
            TG[confa] -= 5
            mis4=[u'щас петь буду',u'да я тебе и без водки спою',u'щас напьюсь и буду буянить']
            mes4=random.choice(mis4)
            reply(type,source,mes4)
            time.sleep(180)
            mis5=[u'я-я-яблоки на сне-е-егу, яплоки на снегу, яплоки нас не пру-у-ут',u'Ой мороз моро-о-оз, не мороззь иа',u'а не буду я петь *NO*',u'ты мне еще начисли, может и спойю']
            mes5=random.choice(mis5)
            reply(type,source,mes5)
        if parameters==u'кофе':
            confa = source[1]
            if TW[confa] > 500:
                reply(type, source, u'Не хочется *NO*')
                return
            if TM[confa] <= 19:
                reply(type,source, u'Недостаточно Коинсов')
                return
            TM[confa] -= 20
            TW[confa] += 70
            TG[confa] -= 5
            reply(type,source,u'*coffee*')
            time.sleep(180)
            reply(type,source,u'пасибо, очень вкусный :)')
        if not parameters:
            reply(type,source,u'ну и че я буду пить с пустой кружки? Глянь, может в холодильнике че есть.')
    else:
        reply(type, source, u'Тамагочик выключен.')

def handler_tam_menu(type,source,parameters):
    reply(type,source,u'В холодильнике у нас:\n*<>*<>*<>*<>*<>*<>*\n  [ Блюда ]\n > Макароны - 50 коин - 200 ед <\n > Супчик - 50 коин - 200 ед <\n > Бутерброд - 20 коин - 70 ед <\n > Вискас - 40 коин - 150 ед <\n > Торт - 30 коин - 80 ед <\n > Чипсы - 25 коин - 50 ед <\n > Каша - 15 коин - 200 ед <\n > Банан - 15 коин - 40 ед <\n > Клубника - 20 коин - 50 ед <\n > Винегрет - 30 коин - 40 ед <\n  [ Напитки ]\n > Кофе - 20 коин - 70 ед <\n > Водка - 40 коин - 300 ед <\n > Вино - 60 коин - 300 ед <\n > Минералка - 40 коин - 150 ед <\n*<>*<>*<>*<>*<>*<>*\nВсего коинсов в чате: '+str(TM[source[1]])+u'\n*<>*<>*<>*<>*<>*<>*')

def hnd_maych(type,source,parameters):
    confa = source[1]
    if confa in A_C_T.keys():
        if parameters==u'мячиком':
            if TI[confa] >= 0:
                if TD[confa] > 500:
                    reply(type, source, u'Не хочется *NO*')
                    return
                else:
                    TD[confa] += 100
                    TG[confa] -= 5
                    msg(source[1],u'/me взяла в лапы мячик и стала катать его по полу, разнося все вокруг =^_^= ')
                    status='dnd'
                    change_bot_status(source[1],u'Разношу все вокруг......',status)
                    time.sleep(600)
                    message = STATUS[source[1]]['message']
                    status = STATUS[source[1]]['status']
                    change_bot_status(source[1], message, status)
                    msg(source[1],u'наигралась я, можно и по спать...')
                    time.sleep(5)
                    status='away'
                    change_bot_status(source[1],u'я сплю *LAZY*',status)
                    time.sleep(2400)
                    message = STATUS[source[1]]['message']
                    status = STATUS[source[1]]['status']
                    change_bot_status(source[1], message, status)
                    msg(source[1],u'мяу :)')
                    return
        if parameters == u'мышкой':
            if TI[confa] >= 10:
                if TENE[confa] > 500:
                    reply(type, source, u'Не хочется *NO*')
                    return
                else:
                    msg(source[1], u'/me гоняюсь за заводной мышкой *CRAZY*')
                    time.sleep(300)
                    TG[confa] -= 5
                    msg(source[1], u'Фух.... Набегалась :)')
                    TD[confa] += 150
                    return
            else:
                reply(type, source, u'Будет доступно с 10 уровня интелекта')
                return
        if parameters == u'компьютер':
            if TI[confa] >= 25:
                if TD[confa] > 500:
                    reply(type, source, u'Не хочется *NO*')
                    return
                else:
                    msg(source[1], u'/me играет на компьютере в Dota')
                    time.sleep(300)
                    msg(source[1], u'Порвали их в тряпки :D')
                    TD[confa] += 200
                    TG[confa] -= 5
                    return
            else:
                reply(type, source, u'Будет доступно с 25 уровня интелекта')
                return
        else:
            reply(type, source, u'читай хелп')
            return
    else:
        reply(type, source, u'Тамагочик выключен.')

def tm_load_now(*list):
        global TM
        try:
                fp = file('dynamic/tm.txt', 'r')
                TM = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/tm.txt', 'w')
                TM = {}
                fp.write( str(TM) )
                fp.close()

def tm_save_now():
        global TM
        fp = file('dynamic/tm.txt', 'w')
        fp.write( str(TM) )
        fp.close()

def tt_load_now(*list):
        global TT
        try:
                fp = file('dynamic/tt.txt', 'r')
                TT = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/tt.txt', 'w')
                TT = {}
                fp.write( str(TT) )
                fp.close()

def tt_save_now():
        global TT
        fp = file('dynamic/tt.txt', 'w')
        fp.write( str(TT) )
        fp.close()

def intelekt_load_now(*list):
        global TI
        try:
                fp = file('dynamic/intelekt.txt', 'r')
                TI = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/intelekt.txt', 'w')
                TI = {}
                fp.write( str(TI) )
                fp.close()

def intelekt_save_now():
        global TI
        fp = file('dynamic/intelekt.txt', 'w')
        fp.write( str(TI) )
        fp.close()

register_stage1_init(tm_load_now)
register_stage1_init(tt_load_now)
register_stage1_init(intelekt_load_now)
register_command_handler(hnd_maych, 'играй', [], 10, 'Играет с тамагочиком, поднимая уровень отдыха, доступные параметры: мячиком, мышкой, компьютер', 'играй мячом', ['играй мячом'])

register_command_handler(handler_tam_eda, 'кушай', [], 10, 'кормит бота. Идея  NESkimos. Написал КОТ', 'доступная еда для бота по команде холодильник', ['кушай кашу'])
register_command_handler(handler_tam_pit, 'пей', [], 10, 'поит бота. Идея NESkimos. написал КОТ', 'доступные напитки смотри в холодильнике по команде холодильник', ['пей минералку'])
register_command_handler(handler_tam_menu, 'холодильник', [], 10, 'показывает список продуктов которыми можно накормить бота', 'холодильник', ['холодильник'])
