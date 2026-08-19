#===istalismanplugin===
# -*- coding: utf-8 -*-

# by Kot

def tort(type,source,nick):
   if nick == handler_botnick(source[1]):
      nick1 = source[2]
      msg(source[1],u'/me запихала '+nick1+' в торт и побежала за ножиком.....')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала торт '+nick1+' с '+str(rand)+' свечами, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me запустила в '+nick+' тортом с '+str(rand)+' свечами, угощайся :) ')

register_command_handler(tort, 'торт', [], 10, 'Угощает юзера тортом', 'торт ник', ['торт Кот'])

def hnd_bossa(type,source,body):
   handler_send_invite(type, source, 'saranskcity@jabber.ru')

register_command_handler(hnd_bossa, 'босса', [], 10, 'Призвать админа бота.', 'босса', ['босса'])

def analgin(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Я не болею :)')
      return
   if not nick:
      reply(type,source,u'Каму тут плоха?')
      return
   msg(source[1],u'/me дала таблеточку анальгина '+nick+', *HOSPITAL* не болей :) ')

register_command_handler(analgin, 'анальгин', [], 10, 'Дать юзеру таблетку анальгина.', 'анальгин ник', ['анальгин Кот'])

def arbyz(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me пригнала телегу '+nick1+' в которой '+str(rand)+' арбузов, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me пригнала '+nick+' телегу  в которой '+str(rand)+' арбузов, угощайся :) ')

register_command_handler(arbyz, 'арбуз', [], 10, 'Угощает юзера арбузом', 'арбуз ник', ['арбуз Кот'])

def baby(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Я выверну ее наизнанку и у меня будет резиновый мужик :-D')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me притаранила '+nick1+' насос и резиновую зину...Приятного времяпрепровождения :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me притаранила '+nick+' насос и резиновую зину...Приятного времяпрепровождения :) ')

register_command_handler(baby, 'бабу', [], 10, 'Дает юзеру резиновую бабу', 'бабу ник', ['бабу Кот'])

def banan(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' бананов, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' бананов, угощайся :) ')

register_command_handler(banan, 'банан', [], 10, 'Угощает юзера бананом', 'банан ник', ['банан Кот'])

def brysnika(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод брусники, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод брусники, угощайся :) ')

register_command_handler(brysnika, 'брусника', [], 10, 'Угощает юзера брусникой', 'брусника ник', ['брусника Кот'])

def shipovnik(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод шиповника, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод шиповника, угощайся :) ')

register_command_handler(shipovnik, 'шиповник', [], 10, 'Угощает юзера шиповником', 'шиповник ник', ['шиповник Кот'])

def chernika(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод черники, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод черники, угощайся :) ')

register_command_handler(chernika, 'черника', [], 10, 'Угощает юзера черникой', 'черника ник', ['черника Кот'])

def cheremyha(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод черемухи, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод черемухи, угощайся :) ')

register_command_handler(cheremyha, 'черемуха', [], 10, 'Угощает юзера черемухой', 'черемуха ник', ['черемуха Кот'])

def fizalis(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод физалиса, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод физалиса, угощайся :) ')

register_command_handler(fizalis, 'брусника', [], 10, 'Угощает юзера физалисом', 'физалис ник', ['физалис Кот'])

def smorodina(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод смородины, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод смородины, угощайся :) ')

register_command_handler(smorodina, 'смородина', [], 10, 'Угощает юзера смородиной', 'смородина ник', ['смородина Кот'])

def ryabina(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод рябины, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод рябины, угощайся :) ')

register_command_handler(ryabina, 'рябина', [], 10, 'Угощает юзера рябиной', 'рябина ник', ['рябина Кот'])

def malina(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод малины, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод малины, угощайся :) ')

register_command_handler(malina, 'малина', [], 10, 'Угощает юзера малиной', 'малина ник', ['малина Кот'])

def kryijovnik(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод крыжовника, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод крыжовника, угощайся :) ')

register_command_handler(kryijovnik, 'крыжовник', [], 10, 'Угощает юзера крыжовником', 'крыжовник ник', ['крыжовник Кот'])

def klukva(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод клюквы, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод клюквы, угощайся :) ')

register_command_handler(klukva, 'клюква', [], 10, 'Угощает юзера клюквой', 'клюква ник', ['клюква Кот'])

def klybnika(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод клубники, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод клубники, угощайся :) ')

register_command_handler(klybnika, 'клубника', [], 10, 'Угощает юзера клубникой', 'клубника ник', ['клубника Кот'])

def ejevika(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод ежевики, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод ежевики, угощайся :) ')

register_command_handler(ejevika, 'ежевика', [], 10, 'Угощает юзера ежевикой', 'ежевика ник', ['ежевика Кот'])

def zemlyanika(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me дала '+nick1+' '+str(rand)+' ягод земляники, угощайся :) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me дала '+nick+' '+str(rand)+' ягод земляники, угощайся :) ')

register_command_handler(zemlyanika, 'земляника', [], 10, 'Угощает юзера земляникой', 'земляника ник', ['земляника Кот'])

def banan1(type,source,nick):
   if nick == handler_botnick(source[1]):
      reply(type,source,u'Пасибо :)')
      return
   if not nick:
      nick1 = source[2]
      rand = random.randrange(1,100)
      msg(source[1], u'/me угостила '+nick1+'  >(///)< барбариской :) , может чай?  ;-) ')
      return
   rand = random.randrange(1,100)
   msg(source[1],u'/me угостила '+nick+' >(///)< барбариской :) , может чай?  ;-) ')

register_command_handler(banan1, 'барбариска', [], 10, 'Угощает юзера барбариской', 'барбариска ник', ['барбариска Кот'])