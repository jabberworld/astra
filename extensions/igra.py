#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

#старт игры
START_IGRA = {}
START_JID = {}
STROIKA_COL = {}
UNIT = {}
col_timer = {}
col_timer_user = {}
#количество ресурсов
WOOD = {}
STONE = {}
IRON = {}
EAT = {}
LUDI = {}

#постройки
PORTAL_COL = {}
WOOD_COL = {}
STONE_COL = {}
IRON_COL = {}
EAT_COL = {}
RATYSHA_COL = {}
KAZARMA_COL = {}
STENA_COL = {}
KYZNICA_COL = {}
RINOK_COL = {}
KONUSHNA_COL ={}
SHKOLA_MAGII = {}
RAZVED_COL = {}
DOM_COL = {}
#армия
ARMIA = {}
mechnik = 'mechnik'
ricar = 'ricar'
mag = 'mag'
lychnik = 'lychnik'
razved = 'razved'
paladin = 'paladin'
jin = 'jin'
dragon = 'dragon'

def reiting(t,s,par):
   jid = handler_jid(s[0])
   if par:
      p = START_IGRA[par]
      if p in START_JID:
         reiting = int(PORTAL_COL[p] + WOOD_COL[p] + STONE_COL[p] + IRON_COL[p] + EAT_COL[p] + RATYSHA_COL[p] + KAZARMA_COL[p] + STENA_COL[p] + KYZNICA_COL[p] + RINOK_COL[p] + KONUSHNA_COL[p] + SHKOLA_MAGII[p] + RAZVED_COL[p] + DOM_COL[p])
         reply(t,s,u'Его рейтинг: '+str(reiting))
         return
   else:
      reiting = int(PORTAL_COL[jid] + WOOD_COL[jid] + STONE_COL[jid] + IRON_COL[jid] + EAT_COL[jid] + RATYSHA_COL[jid] + KAZARMA_COL[jid] + STENA_COL[jid] + KYZNICA_COL[jid] + RINOK_COL[jid] + KONUSHNA_COL[jid] + SHKOLA_MAGII[jid] + RAZVED_COL[jid] + DOM_COL[jid])
      reply(t,s,u'Твой рейтинг: '+str(reiting))
      return

register_command_handler(reiting, 'рейтинг',[], 10, 'Показывает ваш рейтинг', 'рейтинг игрок', ['рейтинг'])

def start_igra(t,s,p):
   jid = handler_jid(s[0])
   nick = s[2]
   if not jid in START_JID:
      if not nick in START_IGRA:
         SHKOLA_MAGII[jid] = 0
         with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))
         START_JID[jid] = nick
         START_IGRA[nick] = jid
         with file('dynamic/start_igra.txt', 'w') as fp: fp.write(str(START_IGRA))
         with file('dynamic/start_jid.txt', 'w') as fp: fp.write(str(START_JID))
         WOOD_COL[jid] = 1
         with file('dynamic/wood_col.txt', 'w') as fp: fp.write(str(WOOD_COL))
         WOOD[jid] = 200
         with file('dynamic/wood.txt', 'w') as fp: fp.write(str(WOOD))
         STONE_COL[jid] = 1
         with file('dynamic/stone_col.txt', 'w') as fp: fp.write(str(STONE_COL))
         STONE[jid] = 200
         with file('dynamic/stone.txt', 'w') as fp: fp.write(str(STONE))
         IRON_COL[jid] = 1
         with file('dynamic/iron_col.txt', 'w') as fp: fp.write(str(IRON_COL))
         IRON[jid] = 200
         with file('dynamic/iron.txt', 'w') as fp: fp.write(str(IRON))
         EAT_COL[jid] = 1
         with file('dynamic/eat_col.txt', 'w') as fp: fp.write(str(EAT_COL))
         EAT[jid] = 200
         LUDI[jid] = 100
         with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
         with file('dynamic/eat.txt', 'w') as fp: fp.write(str(EAT))
         RATYSHA_COL[jid] = 0
         PORTAL_COL[jid] = 0
         with file('dynamic/ratysha_col.txt', 'w') as fp: fp.write(str(RATYSHA_COL))
         with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))
         KAZARMA_COL[jid] = 0
         with file('dynamic/kazarma_col.txt', 'w') as fp: fp.write(str(KAZARMA_COL))
         STENA_COL[jid] = 0
         with file('dynamic/stena_col.txt', 'w') as fp: fp.write(str(STENA_COL))
         RAZVED_COL[jid] = 0
         with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))
         
         ARMIA[jid] = {mechnik: 50, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, dragon: 0, jin: 0}
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, paladin: 0, dragon: 0, jin: 0}
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         reply(t,s,u': Добро пожаловать в игру \n  _-= EPIC FALE! =-_\nЭто военно-экономическая стратегия. Пока ты это читаешь в твоем замке накопится немного ресурсов для улучшения одного из добывающих зданий, построить здание можно командой ПОСТРОИТЬ, например, "построить лесопилка". Кстати говоря, просмотр построеных зданий, их уровень, а так же доступных для постройки в ближайшем будущем Ты можешь осуществить командой ЗДАНИЯ. В зависимости от построеных зданий ты приобретаешь новые возможности в игре. Например, построив стену, Ты повышаешь защиту замка, каждый уровень стены +1 к защите юнита. Построив Казарму, можно начать строить армию. Построив рынок, можно передавать ресурсы другим игрокам и т.д. Если тебе понадобится помощь, ты можешь вызвать меня командой "советник".')
      else:
         reply(t,s,u'Этот ник занят!')
         return
   else:
     reply(t,s,u'Ты и так играешь!')


register_command_handler(start_igra, 'старт', [], 10, 'Вход в игру EPIC FALE', 'старт', ['старт'])

def postroika(t,s,p):
   global STROIKA_COL
   jid = handler_jid(s[0])
   if not jid in STROIKA_COL:
      STROIKA_COL[jid] = 0
   if jid in START_JID:
      if p == u'каменоломня':
         if STROIKA_COL[jid] < 3:
            if STONE_COL[jid] <= 10:
               if STONE[jid] >= 170:
                  if WOOD[jid] >= 220:
                     if IRON[jid] >= 220:
                        if EAT[jid] >= 220:
                           reply(t,s,u'Постройка начата.\Время постройки: 4 часа.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 170
                           WOOD[jid] -= 220
                           IRON[jid] -= 220
                           EAT[jid] -= 220
                           time.sleep(14400)
                           STONE_COL[jid] += 1
                           with file('dynamic/stone_col.txt', 'w') as fp: fp.write(str(STONE_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Каменоломня построена!')
                           msg(jid,u'Каменоломня построена!')
                           return
                        else:
                          reply(t,s,u'Недостаточно еды. Требуется 220')
                          return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 220 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева. Требуется 220 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 170 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u'Нельзя строить одновременно больше трех зданий зданий')
            return
      if p == u'лесопилка':
         if STROIKA_COL[jid] < 3:
            if WOOD_COL[jid] <= 10:
               if STONE[jid] >= 220:
                  if WOOD[jid] >= 170:
                     if IRON[jid] >= 220:
                        if EAT[jid] >= 220:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 220
                           WOOD[jid] -= 170
                           IRON[jid] -= 220
                           EAT[jid] -= 220
                           time.sleep(14400)
                           WOOD_COL[jid] += 1
                           with file('dynamic/wood_col.txt', 'w') as fp: fp.write(str(WOOD_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Лесопилка построена!')
                           msg(jid,u'Лесопилка построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 220 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 220 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева. Требуется 170 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 220 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u'Нельзя строить одновременно больше трех зданий зданий')
            return
      if p == u'шахта':
         if STROIKA_COL[jid] < 3:
            if IRON_COL[jid] <= 10:
               if STONE[jid] >= 220:
                  if WOOD[jid] >= 220:
                     if IRON[jid] >= 170:
                        if EAT[jid] >= 220:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 220
                           WOOD[jid] -= 220
                           IRON[jid] -= 170
                           EAT[jid] -= 220
                           time.sleep(14400)
                           IRON_COL[jid] += 1
                           with file('dynamic/iron_col.txt', 'w') as fp: fp.write(str(IRON_COL))
                           STROIKA_COL[jid] -= 1
                           with file('dynamic/stroika_col.txt', 'w') as fp: fp.write(str(STROIKA_COL))
                           reply(t,s,u'Шахта железной руды построена!')
                           msg(jid,u'Шахта железной руды построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 220 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 170 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 220 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 220 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'ферма':
         if STROIKA_COL[jid] < 3:
            if EAT_COL[jid] <= 10:
               if STONE[jid] >= 220:
                  if WOOD[jid] >= 220:
                     if IRON[jid] >= 220:
                        if EAT[jid] >= 170:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 220
                           WOOD[jid] -= 220
                           IRON[jid] -= 220
                           EAT[jid] -= 170
                           time.sleep(14400)
                           EAT_COL[jid] += 1
                           with file('dynamic/eat_col.txt', 'w') as fp: fp.write(str(EAT_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Ферма построена!')
                           msg(jid,u'Ферма построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 170 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 220 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 220 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 220 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'казарма':
         if STROIKA_COL[jid] < 3:
            if RATYSHA_COL[jid] >= 1:
               if KAZARMA_COL[jid] < 21:
                  if STONE[jid] >= 1420:
                     if WOOD[jid] >= 1420:
                        if IRON[jid] >= 1420:
                           if EAT[jid] >= 1420:
                              reply(t,s,u'Постройка начата.')
                              STROIKA_COL[jid] += 1
                              STONE[jid] -= 1520
                              WOOD[jid] -= 1420
                              IRON[jid] -= 1420
                              EAT[jid] -= 1420
                              time.sleep(15400)
                              KAZARMA_COL[jid] += 1
                              with file('dynamic/kazarma_col.txt', 'w') as fp: fp.write(str(KAZARMA_COL))
                              STROIKA_COL[jid] -= 1
                              reply(t,s,u'Казарма построена!')
                              msg(jid,u'Казарма построена!')
                              return
                           else:
                              reply(t,s,u'Недостаточно еды. Требуется 1420 ')
                              return
                        else:
                           reply(t,s,u'Недостаточно железа. Требуется 1520 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно дерева Требуется 1420 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно камня. Требуется 1420 ')
                     return
               else:
                  reply(t,s,u'Здание имеет максимальный уровень.')
                  return
            else:
               reply(t,s,u'Построй Ратушу')
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'ратуша':
         if STROIKA_COL[jid] < 3:
            if RATYSHA_COL[jid] <=21:
               if STONE[jid] >= 1120:
                  if WOOD[jid] >= 1120:
                     if IRON[jid] >= 1120:
                        if EAT[jid] >= 1120:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 1120
                           WOOD[jid] -= 1120
                           IRON[jid] -= 1120
                           EAT[jid] -= 1120
                           time.sleep(16600)
                           RATYSHA_COL[jid] += 1
                           with file('dynamic/ratysha_col.txt', 'w') as fp: fp.write(str(RATYSHA_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Ратуша построена!')
                           msg(jid,u'Ратуша построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 1120 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 1120 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 1120 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 1120 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'стена':
         if STROIKA_COL[jid] < 3:
            if STENA_COL[jid] <=21:
               if STONE[jid] >= 2120:
                  if WOOD[jid] >= 2120:
                     if IRON[jid] >= 2120:
                        if EAT[jid] >= 2120:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 2120
                           WOOD[jid] -= 2120
                           IRON[jid] -= 2120
                           EAT[jid] -= 2120
                           time.sleep(20400)
                           STENA_COL[jid] += 1
                           with file('dynamic/stena_col.txt', 'w') as fp: fp.write(str(STENA_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Стена построена!')
                           msg(jid,u'Стена построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 2120 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 2120 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 2120 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 2120 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'рынок':
         if not jid in RINOK_COL:
            RINOK_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if RINOK_COL[jid] <= 0:
               if STONE[jid] >= 500:
                  if WOOD[jid] >= 500:
                     if IRON[jid] >= 500:
                        if EAT[jid] >= 500:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 500
                           WOOD[jid] -= 500
                           IRON[jid] -= 500
                           EAT[jid] -= 500
                           time.sleep(7200)
                           RINOK_COL[jid] += 1
                           with file('dynamic/rinok.txt', 'w') as fp: fp.write(str(RINOK_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Рыночная площадь построена!')
                           msg(jid,u'Рыночная площадь построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 500 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 500 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 500 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 500 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'корпус':
         if not jid in RAZVED_COL:
            RAZVED_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if RAZVED_COL[jid] <= 20:
               if STONE[jid] >= 900:
                  if WOOD[jid] >= 900:
                     if IRON[jid] >= 900:
                        if EAT[jid] >= 900:
                           reply(t,s,u'Постройка начата.Здание будет готово через 3 часа.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 900
                           WOOD[jid] -= 900
                           IRON[jid] -= 900
                           EAT[jid] -= 900
                           time.sleep(10200)
                           RAZVED_COL[jid] += 1
                           with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Развед корпус построен!')
                           msg(jid,u'Развед корпус построен!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 900 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 900 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 900 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 900 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'конюшня':
         if not jid in KONUSHNA_COL:
            KONUSHNA_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if KAZARMA_COL[jid] >= 5:
               if KONUSHNA_COL[jid] <= 20:
                  if STONE[jid] >= 1350:
                     if WOOD[jid] >= 1350:
                        if IRON[jid] >= 1350:
                           if EAT[jid] >= 1350:
                              reply(t,s,u'Постройка начата.')
                              STROIKA_COL[jid] += 1
                              STONE[jid] -= 1350
                              WOOD[jid] -= 1350
                              IRON[jid] -= 1350
                              EAT[jid] -= 1350
                              time.sleep(8800)
                              KONUSHNA_COL[jid] += 1
                              with file('dynamic/konushna.txt', 'w') as fp: fp.write(str(KONUSHNA_COL))
                              STROIKA_COL[jid] -= 1
                              reply(t,s,u'Конюшня построена!')
                              msg(jid,u'Конюшня построена!')
                              return
                           else:
                              reply(t,s,u'Недостаточно еды. Требуется 1350 ')
                              return
                        else:
                           reply(t,s,u'Недостаточно железа. Требуется 1350 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно дерева Требуется 1350 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно камня. Требуется 1350 ')
                     return
               else:
                  reply(t,s,u'Здание имеет максимальный уровень.')
                  return
            else:
               reply(t,s,u'Построй Казарму 5 уровня')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'школа':
         if not jid in SHKOLA_MAGII:
            SHKOLA_MAGII[jid] = 0
         if STROIKA_COL[jid] < 3:
            if RATYSHA_COL[jid] >= 10:
               if KAZARMA_COL[jid] >= 10:
                  if SHKOLA_MAGII[jid] <= 20:
                     if STONE[jid] >= 2000:
                        if WOOD[jid] >= 2000:
                           if IRON[jid] >= 2000:
                              if EAT[jid] >= 2000:
                                 reply(t,s,u'Постройка начата.')
                                 STROIKA_COL[jid] += 1
                                 STONE[jid] -= 2000
                                 WOOD[jid] -= 2000
                                 IRON[jid] -= 2000
                                 EAT[jid] -= 2000
                                 time.sleep(11200)
                                 SHKOLA_MAGII[jid] += 1
                                 with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))
                                 STROIKA_COL[jid] -= 1
                                 reply(t,s,u'Школа магии построена!')
                                 msg(jid,u'Школа магии построена!')
                                 return
                              else:
                                 reply(t,s,u'Недостаточно еды. Требуется 2000 ')
                                 return
                           else:
                              reply(t,s,u'Недостаточно железа. Требуется 2000 ')
                              return
                        else:
                           reply(t,s,u'Недостаточно дерева Требуется 2000 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно камня. Требуется 2000 ')
                        return
                  else:
                     reply(t,s,u'Здание имеет максимальный уровень.')
                     return
               else:
                  reply(t,s,u'Построй Казарму 10 уровня')
                  return
            else:
               reply(t,s,u'Построй Ратушу 10 уровня')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'кузница':
         if not jid in KYZNICA_COL:
            KYZNICA_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if KAZARMA_COL[jid] < 5:
               reply(t,s,u'Построй Казарму 5 уровня')
               return
            if KYZNICA_COL[jid] <= 20:
               if STONE[jid] >= 1800:
                  if WOOD[jid] >= 1800:
                     if IRON[jid] >= 1800:
                        if EAT[jid] >= 1800:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 1800
                           WOOD[jid] -= 1800
                           IRON[jid] -= 1800
                           EAT[jid] -= 1800
                           time.sleep(13200)
                           KYZNICA_COL[jid] += 1
                           with file('dynamic/kyznica.txt', 'w') as fp: fp.write(str(KYZNICA_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Кузница построена!')
                           msg(jid,u'Кузница построена!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 1800 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 1800 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 1800 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 1800 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'портал':
         if not jid in PORTAL_COL:
            PORTAL_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if RATYSHA_COL[jid] >= 20:
               reply(t,s,u'Построй Ратушу 20 уровня')
               return
            if PORTAL_COL[jid] <= 20:
               if STONE[jid] >= 5000:
                  if WOOD[jid] >= 5000:
                     if IRON[jid] >= 5000:
                        if EAT[jid] >= 5000:
                           reply(t,s,u'Постройка начата.')
                           STROIKA_COL[jid] += 1
                           STONE[jid] -= 5000
                           WOOD[jid] -= 5000
                           IRON[jid] -= 5000
                           EAT[jid] -= 5000
                           time.sleep(25000)
                           PORTAL_COL[jid] += 1
                           with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))
                           STROIKA_COL[jid] -= 1
                           reply(t,s,u'Портал построен!')
                           msg(jid,u'Портал построен!')
                           return
                        else:
                           reply(t,s,u'Недостаточно еды. Требуется 5000 ')
                           return
                     else:
                        reply(t,s,u'Недостаточно железа. Требуется 5000 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно дерева Требуется 5000 ')
                     return
               else:
                  reply(t,s,u'Недостаточно камня. Требуется 5000 ')
                  return
            else:
               reply(t,s,u'Здание имеет максимальный уровень.')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      if p == u'дом':
         if not jid in DOM_COL:
            DOM_COL[jid] = 0
         if STROIKA_COL[jid] < 3:
            if RATYSHA_COL[jid] < 1:
               reply(t,s,u'Построй Ратушу')
               return
            if STONE[jid] >= 150:
               if WOOD[jid] >= 150:
                  if IRON[jid] >= 150:
                     if EAT[jid] >= 350:
                        reply(t,s,u'Постройка начата.')
                        STROIKA_COL[jid] += 1
                        STONE[jid] -= 150
                        WOOD[jid] -= 150
                        IRON[jid] -= 150
                        EAT[jid] -= 350
                        time.sleep(1800)
                        DOM_COL[jid] += 1
                        with file('dynamic/dom_col.txt', 'w') as fp: fp.write(str(DOM_COL))
                        STROIKA_COL[jid] -= 1
                        LUDI[jid] += 100
                        with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                        reply(t,s,u'Дом построен!')
                        msg(jid,u'Дом построен!')
                        return
                     else:
                        reply(t,s,u'Недостаточно еды. Требуется 5000 ')
                        return
                  else:
                     reply(t,s,u'Недостаточно железа. Требуется 5000 ')
                     return
               else:
                  reply(t,s,u'Недостаточно дерева Требуется 5000 ')
                  return
            else:
               reply(t,s,u'Недостаточно камня. Требуется 5000 ')
               return
         else:
            reply(t,s,u' Нельзя строить одновременно больше трех зданий зданий ')
            return
      else:
         b = p
         zdanie(t,s,b)
         return
   else:
      reply(t,s,u'Начни игру')

def obmen(t,s,p):
   if len(p) >= 3:
      jid = handler_jid(s[0])
      p = p.split()
      user = p[0]
      resurs = p[1]
      col = p[2]
      if jid in START_JID:
         if user in START_IGRA:
            igrok = START_IGRA[user]
            user1 = START_JID[jid]
            if RINOK_COL[jid] >= 1:
               if resurs == u'дерево':
                  if col.isdigit():
                     if WOOD[jid] >= int(col):
                        WOOD[jid] -= int(col)
                        WOOD[igrok] += int(col)
                        msg(s[1],u'Игрок '+user1+u' передал '+str(user)+u' '+str(col)+u' единиц дерева')
                        msg(igrok,u'Игрок '+user1+u' передал тебе '+str(col)+u' единиц дерева')
                        return
                     else:
                        reply(t,s,u'У тебя нет столько дерева')
                        return
                  else:
                     reply(t,s,u'Надо число')
                     return
               if resurs == u'камень':
                  if col.isdigit():
                     if STONE[jid] >= int(col):
                        STONE[jid] -= int(col)
                        STONE[igrok] += int(col)
                        msg(s[1],u'Игрок '+user1+u' передал '+str(user)+u' '+str(col)+u' единиц камня')
                        msg(igrok,u'Игрок '+user1+u' передал тебе '+str(col)+u' единиц камня')
                        return
                     else:
                        reply(t,s,u'У тебя нет столько камня')
                        return
                  else:
                     reply(t,s,u'Надо число')
                     return
               if resurs == u'еда':
                  if col.isdigit():
                     if EAT[jid] >= int(col):
                        EAT[jid] -= int(col)
                        EAT[igrok] += int(col)
                        msg(s[1],u'Игрок '+user1+u' передал '+str(user)+u' '+str(col)+u' единиц еды')
                        msg(igrok,u'Игрок '+user1+u' передал тебе '+str(col)+u' единиц еды')
                        return
                     else:
                        reply(t,s,u'У тебя нет столько еды')
                        return
                  else:
                     reply(t,s,u'Надо число')
                     return
               if resurs == u'железо':
                  if col.isdigit():
                     if IRON[jid] >= int(col):
                        IRON[jid] -= int(col)
                        IRON[igrok] += int(col)
                        msg(s[1],u'Игрок '+user1+u' передал '+str(user)+u' '+str(col)+u' единиц железа')
                        msg(igrok,u'Игрок '+user1+u' передал тебе '+str(col)+u' единиц железа')
                        return
                     else:
                        reply(t,s,u'У тебя нет столько железа')
                        return
                  else:
                     reply(t,s,u'Надо число')
                     return
               else:
                  reply(t,s,u'Нет такого ресурса')
                  return
            else:
               reply(t,s,u'Построй рынок')
               return
         else:
            reply(t,s,u'Игрок не найден')
            return
      else:
         reply(t,s,u'Напиши СТАРТ чтобы начать игру.')
         return
   else:
      reply(t,s,u'недобор параметров\nпиши дать ник дерево 50')

register_command_handler(obmen, 'дать', [], '10', 'Позволяет передавать ресурсы другим игрокам.', ' дать JID дерево 50 ', [' дать JID дерево 50 '])

def zdanie(t,s,b):
   jid = handler_jid(s[0])
   if not jid in DOM_COL:
      DOM_COL[jid] = 0
      with file('dynamic/dom_col.txt', 'w') as fp: fp.write(str(DOM_COL))
   if not jid in PORTAL_COL:
      PORTAL_COL[jid] = 0
      with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))
   if not jid in RINOK_COL:
      RINOK_COL[jid] = 0
      with file('dynamic/rinok.txt', 'w') as fp: fp.write(str(RINOK_COL))
   if not jid in RAZVED_COL:
      RAZVED_COL[jid] = 0
      with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))
   if not jid in KYZNICA_COL:
      KYZNICA_COL[jid] = 0
      with file('dynamic/kyznica.txt', 'w') as fp: fp.write(str(KYZNICA_COL))
   if not jid in KONUSHNA_COL:
      KONUSHNA_COL[jid] = 0
      with file('dynamic/konushna_col.txt', 'w') as fp: fp.write(str(KONUSHNA_COL))
   if not jid in SHKOLA_MAGII:
      SHKOLA_MAGII[jid] = 0
      with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))
   if jid in START_JID:
      repl = 'Твои постройки:'
      if WOOD_COL[jid] > 0:
         repl += u' \n• Лесопилка - '+str(WOOD_COL[jid])+u' уровня'
      else:
         repl += u' \n• Лесопилка - Не построенно.'
      if STONE_COL[jid] > 0:
         repl += u' \n• Каменоломня - '+str(STONE_COL[jid])+u' уровня'
      else:
         repl += u' \n• Каменоломня - Не построенно'
      if IRON_COL[jid] > 0:
         repl += u' \n• Шахта - '+str(IRON_COL[jid])+u' уровня'
      else:
         repl += u' \n• Шахта - не построенно'
      if EAT_COL[jid] > 0:
         repl += u' \n• Ферма - '+str(EAT_COL[jid])+u' уровня'
      else:
         repl += u' \n• Ферма - не построенно'
      if RATYSHA_COL[jid] > 0:
         repl += u' \n• Ратуша - '+str(RATYSHA_COL[jid])+u' уровня'
      else:
         repl += u' \n• Ратуша - не построенно'
      if KAZARMA_COL[jid] > 0:
         repl += u' \n• Казарма - '+str(KAZARMA_COL[jid])+u' уровня'
      else:
         repl += u' \n• Казарма - не построенно'
      if STENA_COL[jid] > 0:
         repl += u' \n• Стена - '+str(STENA_COL[jid])+u' уровня'
      else:
         repl += u' \n• Стена - не построенно'
      if RINOK_COL[jid] > 0:
         repl += u' \n• Рынок - '+str(RINOK_COL[jid])+u' уровня'
      else:
         repl += u' \n• Рынок - не построенно'
      if RINOK_COL[jid] > 0:
         repl += u' \n• Конюшня - '+str(KONUSHNA_COL[jid])+u' уровня'
      else:
         repl += u' \n• Конюшня - не построенно'
      if KYZNICA_COL[jid] > 0:
         repl += u' \n• Кузница - '+str(KYZNICA_COL[jid])+u' уровня'
      else:
         repl += u' \n• Кузница - не построенно'
      if RAZVED_COL[jid] > 0:
         repl += u' \n• Развед корпус - '+str(RAZVED_COL[jid])+u' уровня'
      else:
         repl += u' \n• Развед корпус - не построенно'
      if SHKOLA_MAGII[jid] > 0:
         repl += u' \n• Школа магии - '+str(SHKOLA_MAGII[jid])+u' уровня'
      else:
         repl += u' \n• Школа магии - не построенно'
      if PORTAL_COL[jid] > 0:
         repl += u' \n• Портал - '+str(PORTAL_COL[jid])+u' уровня'
      else:
         repl += u' \n• Портал - не построенно'
      if DOM_COL[jid] > 0:
         repl += u' \n• Дома - '+str(DOM_COL[jid])
      else:
         repl += u' \n• Дома - не построенно'
      reply(t,s,repl)

register_command_handler(zdanie, 'здания', [], 10, 'Показывает ваши здания, уровень развития.', 'здания', ['здания'])

register_command_handler(postroika, 'построить', [], 10, 'Построить здание. ЛЕСОПИЛКА, ШАХТА, КАМЕНОЛОМНЯ, ФЕРМА - повышают добычу ресурсов. КАЗАРМА - позволяет тренировать мечников. СТЕНА - повышает защиту армии в замке. РЫНОК - позволяет обмениваться ресурсами. ', 'Построить лесопилка', ['построить казарма'])

def resi(t,s,p):
   jid = handler_jid(s[0])
   if not jid in LUDI:
      LUDI[jid] = 100
      with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
   if jid in START_JID:
      reply(t,s,u'Ресурсы:\n• Дерево: '+str(WOOD[jid])+u'\n• Камень: '+str(STONE[jid])+u'\n• Железо: '+str(IRON[jid])+u'\n• Еда: '+str(EAT[jid])+u'\n• Население: '+str(LUDI[jid]))
   else:
      reply(t,s,u'Начни играть')

register_command_handler(resi, 'склады', [], 10, 'Показывает количество добытых ресурсов', 'склады', ['склады'])

def igroki(t,s,b):
   reply(t,s,u'Список игроков: \n• '+str.join('\n• ',START_IGRA.keys()))

register_command_handler(igroki, 'игроки', [], 10, 'Показать список играющих', 'игроки', ['игроки'])

def load_start_jid(*list):
        global START_JID
        try:
                with file('dynamic/start_jid.txt', 'r') as fp: START_JID = eval(fp.read())
        except:
                START_JID = {}
                with file('dynamic/start_jid.txt', 'w') as fp: fp.write(str(START_JID))

def load_start_igra(*list):
        global START_IGRA
        try:
                with file('dynamic/start_igra.txt', 'r') as fp: START_IGRA = eval(fp.read())
        except:
                START_IGRA = {}
                with file('dynamic/start_igra.txt', 'w') as fp: fp.write(str(START_IGRA))


def load_wood_col(*list):
        global WOOD_COL
        try:
                with file('dynamic/wood_col.txt', 'r') as fp: WOOD_COL = eval(fp.read())
        except:
                WOOD_COL = {}
                with file('dynamic/wood_col.txt', 'w') as fp: fp.write(str(WOOD_COL))


def load_wood(*list):
        global WOOD
        try:
                with file('dynamic/wood.txt', 'r') as fp: WOOD = eval(fp.read())
        except:
                WOOD = {}
                with file('dynamic/wood.txt', 'w') as fp: fp.write(str(WOOD))

def load_stone_col(*list):
        global STONE_COL
        try:
                with file('dynamic/stone_col.txt', 'r') as fp: STONE_COL = eval(fp.read())
        except:
                STONE_COL = {}
                with file('dynamic/stone_col.txt', 'w') as fp: fp.write(str(STONE_COL))

def load_stone(*list):
        global STONE
        try:
                with file('dynamic/stone.txt', 'r') as fp: STONE = eval(fp.read())
        except:
                STONE = {}
                with file('dynamic/stone.txt', 'w') as fp: fp.write(str(STONE))

def load_iron_col(*list):
        global IRON_COL
        try:
                with file('dynamic/iron_col.txt', 'r') as fp: IRON_COL = eval(fp.read())
        except:
                IRON_COL = {}
                with file('dynamic/iron_col.txt', 'w') as fp: fp.write(str(IRON_COL))

def load_iron(*list):
        global IRON
        try:
                with file('dynamic/iron.txt', 'r') as fp: IRON = eval(fp.read())
        except:
                IRON = {}
                with file('dynamic/iron.txt', 'w') as fp: fp.write(str(IRON))

def load_ludi_col(*list):
        global LUDI
        try:
                with file('dynamic/ludi.txt', 'r') as fp: LUDI = eval(fp.read())
        except:
                LUDI = {}
                with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))

register_stage1_init(load_ludi_col)

def load_eat_col(*list):
        global EAT_COL
        try:
                with file('dynamic/eat_col.txt', 'r') as fp: EAT_COL = eval(fp.read())
        except:
                EAT_COL = {}
                with file('dynamic/eat_col.txt', 'w') as fp: fp.write(str(EAT_COL))

def load_eat(*list):
        global EAT
        try:
                with file('dynamic/eat.txt', 'r') as fp: EAT = eval(fp.read())
        except:
                EAT = {}
                with file('dynamic/eat.txt', 'w') as fp: fp.write(str(EAT))

def load_ratysha_col(*list):
        global RATYSHA_COL
        try:
                with file('dynamic/ratysha_col.txt', 'r') as fp: RATYSHA_COL = eval(fp.read())
        except:
                RATYSHA_COL = {}
                with file('dynamic/ratysha_col.txt', 'w') as fp: fp.write(str(RATYSHA_COL))

def load_kazarma_col(*list):
        global KAZARMA_COL
        try:
                with file('dynamic/kazarma_col.txt', 'r') as fp: KAZARMA_COL = eval(fp.read())
        except:
                KAZARMA_COL = {}
                with file('dynamic/kazarma_col.txt', 'w') as fp: fp.write(str(KAZARMA_COL))

def load_stena_col(*list):
        global STENA_COL
        try:
                with file('dynamic/stena_col.txt', 'r') as fp: STENA_COL = eval(fp.read())
        except:
                STENA_COL = {}
                with file('dynamic/stena_col.txt', 'w') as fp: fp.write(str(STENA_COL))



def load_stroika_col(*list):
        global STROIKA_COL
        try:
                with file('dynamic/stroika_col.txt', 'r') as fp: STROIKA_COL = eval(fp.read())
        except:
                STROIKA_COL = {}
                with file('dynamic/stroika_col.txt', 'w') as fp: fp.write(str(STROIKA_COL))

def load_unit(*list):
        global UNIT
        try:
                with file('dynamic/unit.txt', 'r') as fp: UNIT = eval(fp.read())
        except:
                UNIT = {}
                with file('dynamic/unit.txt', 'w') as fp: fp.write(str(UNIT))

def load_rinok(*list):
        global RINOK_COL
        try:
                with file('dynamic/rinok.txt', 'r') as fp: RINOK_COL = eval(fp.read())
        except:
                RINOK_COL = {}
                with file('dynamic/rinok.txt', 'w') as fp: fp.write(str(RINOK_COL))

def load_razved(*list):
        global RAZVED_COL
        try:
                with file('dynamic/razved.txt', 'r') as fp: RAZVED_COL = eval(fp.read())
        except:
                RAZVED_COL = {}
                with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))

def load_shkola(*list):
        global SHKOLA_MAGII
        try:
                with file('dynamic/shkola.txt', 'r') as fp: SHKOLA_MAGII = eval(fp.read())
        except:
                SHKOLA_MAGII = {}
                with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))

def load_kyznica(*list):
        global KYZNICA_COL
        try:
                with file('dynamic/kyznica.txt', 'r') as fp: KYZNICA_COL = eval(fp.read())
        except:
                KYZNICA_COL = {}
                with file('dynamic/kyznica.txt', 'w') as fp: fp.write(str(KYZNICA_COL))

def load_dom(*list):
        global DOM_COL
        try:
                with file('dynamic/dom_col.txt', 'r') as fp: DOM_COL = eval(fp.read())
        except:
                DOM_COL = {}
                with file('dynamic/dom_col.txt', 'w') as fp: fp.write(str(DOM_COL))

register_stage1_init(load_dom)

def load_portal(*list):
        global PORTAL_COL
        try:
                with file('dynamic/portal_col.txt', 'r') as fp: PORTAL_COL = eval(fp.read())
        except:
                PORTAL_COL = {}
                with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))

register_stage1_init(load_portal)

def load_konushna(*list):
        global KONUSHNA_COL
        try:
                with file('dynamic/konushna.txt', 'r') as fp: KONUSHNA_COL = eval(fp.read())
        except:
                KONUSHNA_COL = {}
                with file('dynamic/konushna.txt', 'w') as fp: fp.write(str(KONUSHNA_COL))


register_stage1_init(load_konushna)
register_stage1_init(load_kyznica)
register_stage1_init(load_shkola)
register_stage1_init(load_razved)
register_stage1_init(load_rinok)


register_stage1_init(load_stena_col)
register_stage1_init(load_kazarma_col)
register_stage1_init(load_ratysha_col)
register_stage1_init(load_eat)
register_stage1_init(load_eat_col)
register_stage1_init(load_iron)
register_stage1_init(load_iron_col)
register_stage1_init(load_stone)
register_stage1_init(load_stone_col)
register_stage1_init(load_wood)
register_stage1_init(load_wood_col)
register_stage1_init(load_start_jid)
register_stage1_init(load_start_igra)