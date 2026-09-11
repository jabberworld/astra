#===istalismanplugin===
# -*- coding: utf-8 -*-

def obechanie(type, source, nick):
        if type == 'public':
                if nick:
                        if nick != handler_botnick(source[1]):
                                if nick in GROUPCHATS[source[1]]:
                                         if source[1] in POL_SEX.keys():
                                                  msg(source[1], u'/me бросил кубики.....')
                                         else:
                                                  msg(source[1], u'/me бросила кубики.....')
                                                  time.sleep(3)
                                                  nick1 = source[2]
                                                  msg(source[1], u'Выпало число: '+random.choice([u'"1" и теперь %s обещает признаться в любви %s',u'"2" и теперь %s обещает купить шоколадку %s',u'"3" и теперь %s обещает поцеловать в засос %s',u'"4" и теперь %s обещает подарить %s подарок',u'"5" и теперь %s обещает поставить фото %s на главную на три дня',u'"6" и теперь %s обещает написать на фото,что любит %s',u'"7" и теперь %s обещает с сегодняшнего дня называть %s Солнышко',u'"8" и теперь %s обещает рассказать анекдот %s',u'"9" и теперь %s обещает быть %s парнем (девушкой)',u'"10" и теперь %s обещает положить 100р. на счёт %s',u'"11" и теперь %s обещает поставить статус,что любишь %s на три дня',u'"12" и теперь %s обещает дать свой логин и пароль %s']) % (source[2], nick))
                                else:
                                        reply(type, source, u'Тут таких нет')
                        else:
                                reply(type, source, u'Щас ты мне наобещаешь, потом не расплатишься!')
                else:
                        reply(type, source, u'сам себе обещать собралсо?!')
        else:
                reply(type, source, u'Нихрена! Только в чате')

register_command_handler(obechanie, 'обещаю', [], 10, 'Обещание', 'обещаю ник', ['обещаю Кот'])