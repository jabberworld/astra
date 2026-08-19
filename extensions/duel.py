#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

INVER_JILET = {}
INVER_BOT = {}
INVER_KASKA = {}
DUEL_LIFE = {}
INVER_BRONIK = {}

def handler_kick111(mType, source, conf, nick, reason):
        IQSender111(mType, source, conf, 'nick', nick, 'role', 'none', nick, reason)

def duel_nick(t,s,b):
   global DUEL_LIFE
   if random.randrange(1, 2) == 2:
      jid = handler_jid(s[0])
      if not jid in DUEL_LIFE:
         DUEL_LIFE[jid] = 100
      DUEL_LIFE[jid] -= 25
      if DUEL_LIFE[jid] >= 1:
         msg(s[1],s[2]+u': Ты ранен!!!\nЗдоровье: '+str(DUEL_LIFE[jid]))
      else:
         user = b
         msg(s[1],user+u': Победа!')
         handler_kick(s[1], s[2], random.choice([u'размазались мозги по стене',u'аста ла виста беби',u'аминь',u'птыдищь',u'бах...дырка в башке',u'может тебе повезет в следующий раз?!',u'пока дырявый юзер',u'прекрасного полета, не будь падение жестоким, жестоким не будь...',u'револьверы детям не игрушки']))
         DUEL_LIFE.clear()
         return
   else:
      jid = handler_jid(s[0])
      if not jid in DUEL_LIFE:
         DUEL_LIFE[jid] = 100
      msg(s[1],s[2]+u': промах \nЗдоровье: '+str(DUEL_LIFE[jid]))


def duel_user(t,s,user):
   global DUEL_LIFE
   if random.randrange(1, 2) == 2:
      mType = t
      source = s
      source[1] = s[1]
      nick = user
      jid1 = handler_jid('%s/%s' % (s[1], nick))
      if not jid1 in DUEL_LIFE:
         DUEL_LIFE[jid1] = 100
      DUEL_LIFE[jid1] -= 25
      if DUEL_LIFE[jid1] >= 1:
         msg(s[1],user+u': Ты ранен!!!\nЗдоровье: '+str(DUEL_LIFE[jid1]))
      else:
         msg(s[1],s[2]+u': Победа!')
         handler_kick111(mType, source, source[1], nick, random.choice([u'размазались мозги по стене',u'аста ла виста беби',u'аминь',u'птыдищь',u'бах...дырка в башке',u'может тебе повезет в следующий раз?!',u'пока дырявый юзер',u'прекрасного полета, не будь падение жестоким, жестоким не будь...',u'револьверы детям не игрушки']))
         DUEL_LIFE.clear()
         return
   else:
      nick = user
      jid1 = handler_jid('%s/%s' % (s[1], nick))
      if not jid1 in DUEL_LIFE:
         DUEL_LIFE[jid1] = 100
      msg(s[1],user+u': промах! \nЗдоровье: '+str(DUEL_LIFE[jid1]))



def duel(t,s,b):
   if not b:
      reply(t,s,u'Нужен ник!')
      return
   args = b.split()
   nick = s[2]
   user = args[0].strip()
   if not user in GROUPCHATS[s[1]]:
      reply(t,s,u'нету его')
      return
   if nick == user:
      reply(t,s,u'Сам в себя чтоли?')
      return
   if user == handler_botnick(s[1]):
      reply(t,s,u'щас тебя расстреляю!')
      return
   else:
      if user_level(s[1]+'/'+nick, s[1]) < 12:
         if user_level(s[1]+'/'+user, s[1]) < 12:
            duel_nick(t,s,b)
            duel_user(t,s,user)
         else:
            reply(t,s,u'Уровень доступа второго дуэлянта должен быть не больше 11')
      else:
         reply(t,s,u'Твой уровень доступа должен быть не больше 11')



def ecipirovka(t,s,b):
   global INVER_JILET
   global INVER_BOT
   global INVER_KASKA
   global INVER_BRONIK
   global DUEL_LIFE
   global BRONIK
   jid = handler_jid(s[0])
   mes = u'На тебе надето:'
   if jid in INVER_KASKA:
      mes += u'\n• Голова: Каска (+25 брони)'
   else:
      mes += u'\n• Голова: -----'
   if jid in INVER_JILET:
      mes += u'\n• Торс: Бр.Жилет (+50 брони)'
   else:
      mes += u'\n• Торс: -----'
   if jid in INVER_BOT:
      mes += u'\n• Ноги: Ботинки (+25 брони)'
   else:
      mes += u'\n• Ноги: -----'
   mes += u'##############\nЗдоровье+Броня: %s + %s' % str(DUEL_LIFE[jid]), str(BRONIK[jid])
   reply(t,s,mes)

def inver_nadet(t,s,b):
   global INVER_JILET
   global INVER_BOT
   global INVER_KASKA
   global INVER_BRONIK
   global DUEL_LIFE
   global BRONIK
   jid = handler_jid(s[0])
   

#regisrer_command_handler(ecipirovka, 'инвентарь', [], 10, '', '', [''])
register_command_handler(duel, 'дуэль', [], 10, 'Вызвать юзера на дуэль, дуэлянт бот', 'дуэль ник', ['дуэль кот'])