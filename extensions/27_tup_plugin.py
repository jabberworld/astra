#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  delirium_plugin.py

#  Idea by metalist<metalist@jabbik.org>

# Code by andreymal<andreymal@jabberon.ru>

import random
users_gadanie={}

def handler_tup(type, source, parameters):
  global users_gadanie
  if not source[0] in users_gadanie.keys():
    lubit=[]
    for i in range(5):
      a=random.randrange(1,20)
      while a in lubit: a=random.randrange(1,20)
      lubit.append(a)

    nelubit=[]
    for i in range(5):
      a=random.randrange(1,20)
      while a in lubit or a in nelubit: a=random.randrange(1,20)
      nelubit.append(a)

    users_gadanie[source[0]]=[lubit,nelubit]
    vybor=lubit+nelubit
    random.shuffle(vybor)
    for i in range(len(vybor)): vybor[i]=str(vybor[i])
    reply(type,source,', '.join(vybor)+'. Выбери одно из чисел!')
  else:
    lubit=users_gadanie[source[0]][0]
    nelubit=users_gadanie[source[0]][1]
    try:
      num=int(parameters.strip())
      if num in lubit:
        reply(type,source,'любит')
        users_gadanie.pop(source[0])
      elif num in nelubit:
        reply(type,source,'не любит')
        users_gadanie.pop(source[0])
      else:
        reply(type,source,'нет такого числа!')
    except: reply(type,source,'идиот, надо число!')

register_command_handler(handler_tup, 'гадание' , ['мук' , 'все'], 10, 'Команда находится в плагине:\ntup_plugin.py\nШуточное гадание на вторую половинку' , 'гадание' , ['гадание'])