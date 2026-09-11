#===istalismanplugin===
# -*- coding: utf-8 -*-

def hnd_podarok(type, source, body):
   if type == 'private':
      reply(type,source,u'Только в чате.')
      return
   mis = [u'коробка шоколадных конфет', u'Набор бокалов',u'Теплый шарфик',u'Ключи от автомобиля TOYOTA',u'Пузырь дорогого коньяка',u'Фоторамка',u'Плазменный Телевизор',u'iPhone 5',u'Ключи от BMW Х ВАСЯ 7, сами немцы таких машин не видели',u'Тушь',u'Губная помада',u'Два билета в кино',u'открытка в которой 500$']
   mes = random.choice(mis)
   if source[1] not in POL_SEX.keys():
      msg(source[1], u'Подарила подарок '+body+' \nОткрывай быстрее!!!\nА там у нас '+mes)
   else:
      msg(source[1], u'Подарил подарок '+body+' \nОткрывай быстрее!!!\nА там у нас '+mes)

register_command_handler(hnd_podarok, 'подарок', [], 10, 'Дарит подарок юзеру.', 'подарок ник', ['подарок чувак'])