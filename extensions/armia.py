#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

coli = {}
colix = {}

def armia(t,s,p):
   jid = handler_jid(s[0])
   if not p:
      if jid not in ARMIA:
         ARMIA[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
      if not jid in col_timer:
         col_timer[jid] = 0
      if col_timer[jid] > 0:
         timer_col1 = int(time.time() - col_timer[jid])
         timer_col = int(10800 - timer_col1)
         timer_col_min = int(timer_col) / 60
         repl = u'\n-----\n Приближается армия от игрока '+str(col_timer_user[jid])+u' через '+str(timer_col_min)+u' мин'
      else:
         repl = '\n-----\n Приближающихся армий нет.'
      reply(t,s,u'Твоя Армия: \nМечники: '+str(ARMIA[jid][mechnik])+u'\nРыцари: '+str(ARMIA[jid][ricar])+u'\nЛучники: '+str(ARMIA[jid][lychnik])+u'\nПаладины: '+str(ARMIA[jid][paladin])+u'\nРазведчики: '+str(ARMIA[jid][razved])+u'\nМаги: '+str(ARMIA[jid][mag])+u'\nДжины: '+str(ARMIA[jid][jin])+u'\nДраконы: '+str(ARMIA[jid][dragon])+repl+u' \n-----')#\n Укажи параметр "*" для получения описания юнита')
      return
#   if p == u'*':
#      repl = u'••• Мечники: \n• Атака: 15\n• Защита: 5\n• Жизнь: 15\n• Грузоподъемность: 6\n•••Стоимость:\n• Дерево: 40\n• Камень: 30\n• Железо: 50\n• Еда: 20\n• Время тренировки: 20 мин\n-----\nЛегкий пеший воин.'
#      repl += u'\n••• Разведчики: \n• Атака: 5\n• Защита: 5\n• Жизнь: 20\n• Грузоподъемность: 0\n•••Стоимость:\n• Дерево: 55\n• Камень: 45\n• Железо: 65\n• Еда: 35\n• Время тренировки: 26 мин\n-----\nРазведчик'
#      reply(t,s,repl)

register_command_handler(armia, 'армия', [], 10, 'Показывает количество вашей армии.', 'армия', ['армия *'])

def unit(t,s,p):
   global UNIT
   jid = handler_jid(s[0])
   if not jid in UNIT:
      UNIT[jid] = 0
   if not p:
      
      reply(t,s,u'Укажи вид юнита')
      return
   if jid in START_JID:
      p = p.split()
      if len(p) < 2:
         if p[0] in [u'мечник', u'лучник', u'рыцарь', u'паладин', u'маг', u'разведчик', u'джин', u'дракон'] and p[0] not in [u'*']:
            reply(t,s,u'Укажи число меньшее количества населения в Замке.')
            return
      #x = int(p[1])
      if p[0] == u'маг':
         if UNIT[jid] < 1:
            #if not p[1]:
            #   reply(t,s,u'Укажи число которое меньше количества населения твоего замка!')
            #   return
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 15:
                  if KONUSHNA_COL < 10:
                     reply(t,s,u'Построй Конюшню 10 уровня')
                     return
                  if SHKOLA_MAGII[jid] < 10:
                     reply(t,s,u'Построй Школу 10 уровня')
                     return
                  if STONE[jid] > int(x) * 55 and IRON[jid] > int(x) * 70 and EAT[jid] > int(x) * 80 and WOOD[jid] > int(x) * 50 and LUDI[jid] - int(x) > 0:
                     STONE[jid] -= int(p[1]) * 55
                     WOOD[jid] -= int(p[1]) * 50
                     IRON[jid] -= int(p[1]) * 70
                     LUDI[jid] -= int(p[1])
                     with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                     EAT[jid] -= int(p[1]) * 50
                     reply(t,s,u'Тренировка Магов начата')
                     coli[jid] = 0
                     UNIT[jid] = 1
                     for x in range(int(x)):
                        time.sleep(2400)
                        ARMIA[jid][mag] += 1
                        coli[jid] += 1
                        with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                        #msg(jid,u'Тренировано Паладинов: '+str(col))
                     reply(t,s,u'Тренировка Магов закончена: '+str(coli[jid]))
                     UNIT[jid] = 0
                     del coli[jid]
                     return
                  else:
                     reply(t,s,u'Недостаточно ресурсов')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 15 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'мечник':
         if UNIT[jid] < 1:
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 1:
                  if STONE[jid] > int(x) * 30 and IRON[jid] > int(x) * 50 and EAT[jid] > int(x) * 20 and WOOD[jid] > int(x) * 30 and LUDI[jid] - int(x) > 0:
                     STONE[jid] -= int(p[1]) * 30
                     WOOD[jid] -= int(p[1]) * 40
                     IRON[jid] -= int(p[1]) * 50
                     LUDI[jid] -= int(p[1])
                     with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                     EAT[jid] -= int(p[1]) * 20
                     reply(t,s,u'Тренировка мечников начата')
                     coli[jid] = 0
                     UNIT[jid] = 1
                     for x in range(int(x)):
                        time.sleep(210)
                        ARMIA[jid][mechnik] += 1
                        coli[jid] += 1
                        with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                        #msg(jid,u'Тренировано Мечников: '+str(col))
                     reply(t,s,u'Тренировка Мечников закончена: '+str(coli[jid]))
                     UNIT[jid] = 0
                     del coli[jid]
                     return
                  else:
                     reply(t,s,u'Недостаточно ресурсов')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 1 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'разведчик':
         if UNIT[jid] < 1:
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 3:
                  if RAZVED_COL[jid] >= 5:
                     if STONE[jid] > int(x) * 45 and IRON[jid] > int(x) * 65 and EAT[jid] > int(x) * 35 and WOOD[jid] > int(x) * 45 and LUDI[jid] - int(x) > 0:
                        STONE[jid] -= int(p[1]) * 45
                        WOOD[jid] -= int(p[1]) * 40
                        IRON[jid] -= int(p[1]) * 65
                        EAT[jid] -= int(p[1]) * 35
                        LUDI[jid] -= int(p[1])
                        with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                        reply(t,s,u'Тренировка разведчиков начата')
                        coli[jid] = 0
                        UNIT[jid] = 1
                        for x in range(int(x)):
                           time.sleep(600)
                           ARMIA[jid][razved] += 1
                           coli[jid] += 1
                           with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                           #msg(jid,u'Тренировано Разведчиков: '+str(col))
                        reply(t,s,u'Тренировка Разведчиков закончена: '+str(coli[jid]))
                        UNIT[jid] = 0
                        del coli[jid]
                        return
                     else:
                        reply(t,s,u'Недостаточно ресурсов')
                        return
                  else:
                     reply(t,s,u'Построй развед корпус 5 уровня')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 3 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'лучник':
         if UNIT[jid] < 1:
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 3:
                  if STONE[jid] > int(x) * 40 and IRON[jid] > int(x) * 45 and EAT[jid] > int(x) * 25 and WOOD[jid] > int(x) * 50 and LUDI[jid] - int(x) > 0:
                     STONE[jid] -= int(p[1]) * 40
                     WOOD[jid] -= int(p[1]) * 50
                     IRON[jid] -= int(p[1]) * 45
                     LUDI[jid] -= int(p[1])
                     with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                     EAT[jid] -= int(p[1]) * 25
                     reply(t,s,u'Тренировка лучников начата')
                     coli[jid] = 0
                     UNIT[jid] = 1
                     for x in range(int(x)):
                        time.sleep(360)
                        ARMIA[jid][lychnik] += 1
                        coli[jid] += 1
                        with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                        #msg(jid,u'Тренировано Лучников: '+str(col))
                     reply(t,s,u'Тренировка Лучников закончена: '+str(coli[jid]))
                     UNIT[jid] = 0
                     del coli[jid]
                     return
                  else:
                     reply(t,s,u'Недостаточно ресурсов')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 3 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'рыцарь':
         if UNIT[jid] < 1:
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 8:
                  if KONUSHNA_COL < 3:
                     reply(t,s,u'Построй Конюшню 3 уровня')
                     return
                  if STONE[jid] > int(x) * 40 and IRON[jid] > int(x) * 90 and EAT[jid] > int(x) * 60 and WOOD[jid] > int(x) * 30 and LUDI[jid] - int(x) > 0:
                     STONE[jid] -= int(p[1]) * 40
                     WOOD[jid] -= int(p[1]) * 30
                     IRON[jid] -= int(p[1]) * 90
                     LUDI[jid] -= int(p[1])
                     with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                     EAT[jid] -= int(p[1]) * 60
                     reply(t,s,u'Тренировка Рыцарей начата')
                     coli[jid] = 0
                     UNIT[jid] = 1
                     for x in range(int(x)):
                        time.sleep(1500)
                        ARMIA[jid][ricar] += 1
                        coli[jid] += 1
                        with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                        #msg(jid,u'Тренировано Рыцарей: '+str(col))
                     reply(t,s,u'Тренировка Рыцарей закончена: '+str(coli[jid]))
                     UNIT[jid] = 0
                     del coli[jid]
                     return
                  else:
                     reply(t,s,u'Недостаточно ресурсов')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 8 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'паладин':
         if UNIT[jid] < 1:
            x = int(p[1])
            colix[jid] = x
            if p[1].isdigit():
               if KAZARMA_COL[jid] >= 15:
                  if KONUSHNA_COL < 10:
                     reply(t,s,u'Построй Конюшню 10 уровня')
                     return
                  if SHKOLA_MAGII[jid] < 5:
                     reply(t,s,u'Построй Школу 5 уровня')
                     return
                  if STONE[jid] > int(x) * 80 and IRON[jid] > int(x) * 150 and EAT[jid] > int(x) * 210 and WOOD[jid] > int(x) * 60 and LUDI[jid] - int(x) > 0:
                     STONE[jid] -= int(p[1]) * 80
                     WOOD[jid] -= int(p[1]) * 60
                     IRON[jid] -= int(p[1]) * 150
                     LUDI[jid] -= int(p[1])
                     with file('dynamic/ludi.txt', 'w') as fp: fp.write(str(LUDI))
                     EAT[jid] -= int(p[1]) * 210
                     reply(t,s,u'Тренировка Паладинов начата')
                     coli[jid] = 0
                     UNIT[jid] = 1
                     for x in range(int(x)):
                        time.sleep(1800)
                        ARMIA[jid][paladin] += 1
                        coli[jid] += 1
                        with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                        #msg(jid,u'Тренировано Паладинов: '+str(col))
                     reply(t,s,u'Тренировка Паладинов закончена: '+str(coli[jid]))
                     UNIT[jid] = 0
                     del coli[jid]
                     return
                  else:
                     reply(t,s,u'Недостаточно ресурсов')
                     return
               else:
                  reply(t,s,u'Требуется Казарма не ниже 15 уровня.')
                  return
            else:
               reply(t,s,u'Укажи количество юнитов')
               return
         else:
            reply(t,s,u'Одновременно можно тренировать только один вид войск')
            return
      if p[0] == u'*':
         if jid in coli:
            if coli[jid] >= 0:
               reply(t,s,u'Построенно '+str(coli[jid])+u' из '+str(colix[jid])+u' юнитов')
               return
            #else:
            #   reply(t,s,u'Нет тренировки юнитов.')
            #   return
         else:
            reply(t,s,u'Нет текущих тренировок')
            return
      else:
         reply(t,s,u'Доступны мечник, лучник, рыцарь, паладин, маг, разведчик, джин, дракон')
         return
   else:
      return

register_command_handler(unit, 'тренировать', [], 10, 'Тренирует армию. С параметром * покажет кол-во тренированных юнитов.', 'тренировать юнит число', ['тренировать мечник 10'])


def war(t,s,par):
   global ARMIA
   if not par:
      reply(t,s,u'На кого нападать собралсо?\n\nПосмотри список игроков командой ИГРОКИ')
      return
   par = par.split()
   if len(par) < 3:
      reply(t,s,u'пиши так: атака ник юнит кол-во')
      return
   #par = par.split()
   if not par[0] in START_IGRA:
      reply(t,s,u'Игровой ник не найден')
      return
   
   jid = handler_jid(s[0])
   igrok = START_IGRA[par[0]]
   #atak = int(par[2])
   if not par[2].isdigit() or not par[2]:
      reply(t,s,u'Количество армии надо указать числом')
      return
   atak = int(par[2])
   if not par[0] in START_IGRA:
      reply(t,s,u'Игрок не найден смотри команду ИГРОКИ')
      return
   if par[1] in [u'мечник']:
      x_arm = mechnik
      gryz = 6
      arm_col1 = 20
      zachita_jid = 20
      yron = 15 * atak
      
   elif par[1] in [u'лучник']:
      x_arm = lychnik
      gryz = 6
      arm_col1 = 25
      zachita_jid = 25
      yron = 5 * atak
   elif par[1] in [u'рыцарь']:
      x_arm = ricar
      zachita_jid = 65
      gryz = 8
      arm_col1 = 65
      yron = 30 * atak
   elif par[1] in [u'маг']:
      x_arm = mag
      gryz = 7
      arm_col1 = 30
      zachita_jid = 30
      yron = int(30 * par[2])
   elif par[1] in [u'паладин']:
      x_arm = paladin
      gryz = 11
      arm_col1 = 85
      zachita_jid = 85
      yron = 45 * atak
   elif par[1] in [u'джин']:
      x_arm = jin
      gryz = 3
      arm_col1 = 210
      zachita_jid = 210
      yron = 90 * atak
   elif par[1] in [u'дракон']:
      x_arm = dragon
      zachita_jid = 480
      gryz = 15
      arm_col1 = 480
      yron = 150 * atak
   else:
      reply(t,s,u'Нет такого юнита! Командуй АРМИЯ')
      return
   igrok = START_IGRA[par[0]]
   if not igrok in GARNIZ:
      GARNIZ[igrok] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
   arm = int(par[2])
   if int(arm) > ARMIA[jid][x_arm]:
      reply(t,s,u'Указанное число больще чем твоя армия!')
      return
   stena = int(STENA_COL[igrok])
   
   ARMIA[jid][x_arm] -= int(arm)
   msg(igrok,u'Игрок '+START_JID[jid]+u' напал на тебя! Его армия прибудет к тебе в течении трех часов!!!')
   reply(t,s,u'Армия отправлена в бой')
   if not igrok in col_timer:
      col_timer[igrok] = 0
   col_timer_user[igrok] = START_JID[jid]
   col_timer[igrok] = time.time()
   #ttttt
   time.sleep(10800)
   col_timer[igrok] = 0
   if GARNIZ[igrok][mechnik] != 0:
      zachita = int(stena + 20)
      zachita_col = int(zachita * GARNIZ[igrok][mechnik])
      arm_col = 20
      ataka_igrok = 15
      xxx = mechnik
   elif GARNIZ[igrok][lychnik] != 0:
      zachita = int(stena + 30)
      arm_col = 15
      ataka_igrok = 5
      xxx = lychnik
      zachita_col = int(zachita * GARNIZ[igrok][lychnik])
   elif GARNIZ[igrok][ricar] != 0:
      zachita = int(stena + 65)
      arm_col = 40
      xxx = ricar
      ataka_igrok = 30
      zachita_col = int(zachita * GARNIZ[igrok][ricar])
   elif GARNIZ[igrok][paladin] != 0:
      zachita = int(stena + 85)
      arm_col = 50
      xxx = paladin
      ataka_igrok = 45
      zachita_col = int(zachita * GARNIZ[igrok][paladin])
   elif GARNIZ[igrok][mag] != 0:
      arm_col = 20
      xxx = mag
      ataka_igrok = 25
      zachita = int(stena + 30)
      zachita_col = int(zachita * GARNIZ[igrok][mag])
   elif GARNIZ[igrok][jin] != 0:
      xxx = jin
      zachita = int(stena + 210)
      arm_col = 100
      ataka_igrok = 90
      zachita_col = int(zachita * GARNIZ[igrok][jin])
   elif GARNIZ[igrok][dragon] != 0:
      zachita = int(stena + 480)
      arm_col = 300
      ataka_igrok = 150
      xxx = dragon
      zachita_col = int(zachita * GARNIZ[igrok][dragon])
      
   else:
      if STONE[igrok] >= 0 and WOOD[igrok] >= 0 and EAT[igrok] >= 0 and IRON[igrok] >= 0:
         EAT[igrok] -= int(arm * gryz)
         WOOD[igrok] -= int(arm * gryz)
         IRON[igrok] -= int(arm * gryz)
         STONE[igrok] -= int(arm * gryz)
         STONE[jid] += int(arm * gryz)
         WOOD[jid] += int(arm * gryz)
         EAT[jid] += int(arm * gryz)
         IRON[jid] += int(arm * gryz)
         arm3 = int(arm * gryz)
      if STONE[igrok] <= 0 and WOOD[igrok] <= 0 and EAT[igrok] <= 0 and IRON[igrok] <= 0:
         EAT[igrok] = 0
         WOOD[igrok] = 0
         IRON[igrok] = 0
         STONE[igrok] = 0
      rezdan = ''
      repl = ''
      if x_arm in [dragon, mag, paladin, jin]:
         postroiki = [PORTAL_COL, WOOD_COL, STONE_COL, IRON_COL, EAT_COL, RATYSHA_COL, KAZARMA_COL, STENA_COL, KYZNICA_COL, RINOK_COL, KONUSHNA_COL, SHKOLA_MAGII, RAZVED_COL, DOM_COL]
         unzdan = random.choice(postroiki)
         if unzdan == PORTAL_COL:
            if PORTAL_COL[igrok] > 0:
               PORTAL_COL[igrok] -= 1
               with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))
               rezdan = u' \nБыло разрушено здание - Портал'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == WOOD_COL:
            if WOOD_COL[igrok] > 1:
               WOOD_COL[igrok] -= 1
               with file('dynamic/wood_col.txt', 'w') as fp: fp.write(str(WOOD_COL))
               rezdan = u' \nБыло разрушено здание - Лесопилка'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == STONE_COL:
            if STONE_COL[igrok] > 1:
               STONE_COL[igrok] -= 1
               with file('dynamic/stone_col.txt', 'w') as fp: fp.write(str(STONE_COL))
               rezdan = u' \nБыло разрушено здание - Каменоломня'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == IRON_COL:
            if IRON_COL[igrok] > 1:
               IRON_COL[igrok] -= 1
               with file('dynamic/iron_col.txt', 'w') as fp: fp.write(str(IRON_COL))
               rezdan = u' \nБыло разрушено здание - Шахта'
         if unzdan == EAT_COL:
            if EAT_COL[igrok] > 1:
               EAT_COL[igrok] -= 1
               with file('dynamic/eat_col.txt', 'w') as fp: fp.write(str(EAT_COL))
               rezdan = u' \nБыло разрушено здание - ферма'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == KAZARMA_COL:
            if KAZARMA_COL[igrok] > 0:
               KAZARMA_COL[igrok] -= 1
               with file('dynamic/kazarma_col.txt', 'w') as fp: fp.write(str(KAZARMA_COL))
               rezdan = u' \nБыло разрушено здание - Казарма'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == RATYSHA_COL:
            if RATYSHA_COL[igrok] > 0:
               RATYSHA_COL[igrok] -= 1
               with file('dynamic/ratysha_col.txt', 'w') as fp: fp.write(str(RATYSHA_COL))
               rezdan = u' \nБыло разрушено здание - Ратуша'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == KYZNICA_COL:
            if KYZNICA_COL[igrok] > 0:
               KYZNICA_COL[igrok] -= 1
               with file('dynamic/kyznica.txt', 'w') as fp: fp.write(str(KYZNICA_COL))
               rezdan = u' \nБыло разрушено здание - Кузница'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == RINOK_COL:
            if RINOK_COL[igrok] > 0:
               RINOK_COL[igrok] -= 1
               with file('dynamic/rinok.txt', 'w') as fp: fp.write(str(RINOK_COL))
               rezdan = u' \nБыло разрушено здание - рынок'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == KONUSHNA_COL:
            if KONUSHNA_COL[igrok] > 0:
               KONUSHNA_COL[igrok] -= 1
               with file('dynamic/konushna.txt', 'w') as fp: fp.write(str(KONUSHNA_COL))
               rezdan = u' \nБыло разрушено здание - Конюшня'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == DOM_COL:
            if DOM_COL[igrok] > 0:
               DOM_COL[igrok] -= 1
               with file('dynamic/dom_col.txt', 'w') as fp: fp.write(str(DOM_COL))
               rezdan = u' \nБыло разрушено здание - Дом'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == SHKOLA_MAGII:
            if SHKOLA_MAGII[igrok] > 0:
               SHKOLA_MAGI[igrok] -= 1
               with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))
               rezdan = u' \nБыло разрушено здание - Школа Магии'
         if unzdan == STENA_COL:
            if STENA_COL[igrok] > 0:
               STENA_COL[igrok] -= 1
               with file('dynamic/stena_col.txt', 'w') as fp: fp.write(str(STENA_COL))
               rezdan = u' \nБыло разрушено здание - Стена'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
         if unzdan == RAZVED_COL:
            if RAZVED_COL[igrok] > 0:
               RAZVED_COL[igrok] -= 1
               with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))
               rezdan = u' \nБыло разрушено здание - Развед Корпус'
            else:
               rezdan = u'\nАтака на постройки не удалась!'
      ARMIA[jid][x_arm] += int(arm)
      reply(t,s,u'Блестящая победа!\nПотери атаки: 0\nПотери защиты: в Замке отсутствуют армии \nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3)+rezdan)
      msg(igrok,u'Поражение!\nПотери атаки: 0\nПотери защиты: в Замке отсутствуют армии \nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3)+rezdan)
      return
   col_lose = GARNIZ[igrok][xxx]
   
   war = int(zachita_col - yron)
   igrok_unit = int(war / zachita)
   if igrok_unit <= 0:
      GARNIZ[igrok][xxx] = 0
      ARMIA[jid][x_arm] += int(arm)
      with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
      with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
      if STONE[igrok] >= 0 and WOOD[igrok] >= 0 and EAT[igrok] >= 0 and IRON[igrok] >= 0:
         EAT[igrok] -= int(arm * gryz)
         WOOD[igrok] -= int(arm * gryz)
         IRON[igrok] -= int(arm * gryz)
         STONE[igrok] -= int(arm * gryz)
         STONE[jid] += int(arm * gryz)
         WOOD[jid] += int(arm * gryz)
         EAT[jid] += int(arm * gryz)
         IRON[jid] += int(arm * gryz)
         arm3 = int(arm * gryz)
         if STONE[igrok] <= 0 and WOOD[igrok] <= 0 and EAT[igrok] <= 0 and IRON[igrok] <= 0:
            EAT[igrok] = 0
            WOOD[igrok] = 0
            IRON[igrok] = 0
            STONE[igrok] = 0
         repl = ''
         rezdan = ''
         if x_arm in [dragon, mag, paladin, jin]:
            postroiki = [PORTAL_COL, WOOD_COL, STONE_COL, IRON_COL, EAT_COL, RATYSHA_COL, KAZARMA_COL, STENA_COL, KYZNICA_COL, RINOK_COL, KONUSHNA_COL, SHKOLA_MAGII, RAZVED_COL, DOM_COL]
            unzdan = random.choice(postroiki)
            if unzdan == PORTAL_COL:
               if PORTAL_COL[igrok] > 0:
                  PORTAL_COL[igrok] -= 1
                  with file('dynamic/portal_col.txt', 'w') as fp: fp.write(str(PORTAL_COL))
                  rezdan = u' \nБыло разрушено здание - Портал'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == WOOD_COL:
               if WOOD_COL[igrok] > 1:
                  WOOD_COL[igrok] -= 1
                  with file('dynamic/wood_col.txt', 'w') as fp: fp.write(str(WOOD_COL))
                  rezdan = u' \nБыло разрушено здание - Лесопилка'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == STONE_COL:
               if STONE_COL[igrok] > 1:
                  STONE_COL[igrok] -= 1
                  with file('dynamic/stone_col.txt', 'w') as fp: fp.write(str(STONE_COL))
                  rezdan = u' \nБыло разрушено здание - Каменоломня'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == IRON_COL:
               if IRON_COL[igrok] > 1:
                  IRON_COL[igrok] -= 1
                  with file('dynamic/iron_col.txt', 'w') as fp: fp.write(str(IRON_COL))
                  rezdan = u' \nБыло разрушено здание - Шахта'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == EAT_COL:
               if EAT_COL[igrok] > 1:
                  EAT_COL[igrok] -= 1
                  with file('dynamic/eat_col.txt', 'w') as fp: fp.write(str(EAT_COL))
                  rezdan = u' \nБыло разрушено здание - ферма'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == KAZARMA_COL:
               if KAZARMA_COL[igrok] > 0:
                  KAZARMA_COL[igrok] -= 1
                  with file('dynamic/kazarma_col.txt', 'w') as fp: fp.write(str(KAZARMA_COL))
                  rezdan = u' \nБыло разрушено здание - Казарма'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == RATYSHA_COL:
               if RATYSHA_COL[igrok] > 0:
                  RATYSHA_COL[igrok] -= 1
                  with file('dynamic/ratysha_col.txt', 'w') as fp: fp.write(str(RATYSHA_COL))
                  rezdan = u' \nБыло разрушено здание - Ратуша'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == KYZNICA_COL:
               if KYZNICA_COL[igrok] > 0:
                  KYZNICA_COL[igrok] -= 1
                  with file('dynamic/kyznica.txt', 'w') as fp: fp.write(str(KYZNICA_COL))
                  rezdan = u' \nБыло разрушено здание - Кузница'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == RINOK_COL:
               if RINOK_COL[igrok] > 0:
                  RINOK_COL[igrok] -= 1
                  with file('dynamic/rinok.txt', 'w') as fp: fp.write(str(RINOK_COL))
                  rezdan = u' \nБыло разрушено здание - рынок'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == KONUSHNA_COL:
               if KONUSHNA_COL[igrok] > 0:
                  KONUSHNA_COL[igrok] -= 1
                  with file('dynamic/konushna.txt', 'w') as fp: fp.write(str(KONUSHNA_COL))
                  rezdan = u' \nБыло разрушено здание - Конюшня'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == DOM_COL:
               if DOM_COL[igrok] > 0:
                  DOM_COL[igrok] -= 1
                  with file('dynamic/dom_col.txt', 'w') as fp: fp.write(str(DOM_COL))
                  rezdan = u' \nБыло разрушено здание - Дом'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == SHKOLA_MAGII:
               if SHKOLA_MAGII[igrok] > 0:
                  SHKOLA_MAGI[igrok] -= 1
                  with file('dynamic/shkola.txt', 'w') as fp: fp.write(str(SHKOLA_MAGII))
                  rezdan = u' \nБыло разрушено здание - Школа Магии'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == STENA_COL:
               if STENA_COL[igrok] > 0:
                  STENA_COL[igrok] -= 1
                  with file('dynamic/stena_col.txt', 'w') as fp: fp.write(str(STENA_COL))
                  rezdan = u' \nБыло разрушено здание - Стена'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
            if unzdan == RAZVED_COL:
               if RAZVED_COL[igrok] > 0:
                  RAZVED_COL[igrok] -= 1
                  with file('dynamic/razved.txt', 'w') as fp: fp.write(str(RAZVED_COL))
                  rezdan = u'\nБыло разрушено здание - Развед Корпус'
               else:
                  rezdan = u'\nАтака на здания не удалась!'
         reply(t,s,u'Блестящая победа!\nПотери атаки: 0\nПотери защиты: '+str(col_lose)+u'\nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3)+rezdan)
         msg(igrok,u'Поражение!\nПотери атаки: 0\nПотери защиты: '+str(col_lose)+u'\nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3)+rezdan)
         return
   else:
      poteri_igrok = int(GARNIZ[igrok][xxx] - igrok_unit)
      war1 = int(zachita_jid * arm) - int(igrok_unit * ataka_igrok)
      arm1 = int(war1 / arm_col1)
      if arm1 <= 0:
         GARNIZ[igrok][xxx] = int(igrok_unit)
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         reply(t,s,u'Поражение! Его армия оказалась сильнее\n Потери атаки: '+str(arm))
         
         msg(igrok,u'Победа! Твоя армия оказалась сильнее\n Потери атаки: '+str(arm))
         return
      arm2 = int(arm - arm1)
      ARMIA[jid][x_arm] += int(arm1)
      GARNIZ[igrok][xxx] = int(igrok_unit)
      with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
      with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
      if STONE[igrok] > 0 and WOOD[igrok] > 0 and EAT[igrok] > 0 and IRON[igrok] > 0:
         EAT[igrok] -= int(arm * gryz)
         WOOD[igrok] -= int(arm * gryz)
         IRON[igrok] -= int(arm * gryz)
         STONE[igrok] -= int(arm * gryz)
         STONE[jid] += int(arm * gryz)
         WOOD[jid] += int(arm * gryz)
         EAT[jid] += int(arm * gryz)
         IRON[jid] += int(arm * gryz)
         arm3 = int(arm * gryz)
         if STONE[igrok] <= 0 and WOOD[igrok] <= 0 and EAT[igrok] <= 0 and IRON[igrok] <= 0:
            EAT[igrok] = 0
            WOOD[igrok] = 0
            IRON[igrok] = 0
            STONE[igrok] = 0
         reply(t,s,u'Отличная победа! \nПотери атаки: '+str(arm2)+u'\nПотери защиты: '+str(poteri_igrok)+u'\nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3))
         msg(igrok,u'Поражение! \nПотери атаки: '+str(arm2)+u'\nПотери защиты: '+str(poteri_igrok)+u'\nБыло украдено ресурсов: Дерево: '+str(arm3)+u' \nКамень: '+str(arm3)+u' \nЖелезо: '+str(arm3)+u' \nЕда: '+str(arm3))
         return

register_command_handler(war, 'атака', [], 10, 'Нападение на другого игрока', 'атака ник количество', ['атака Вася мечник 150'])

def podkrep(t,s,par):
   jid = handler_jid(s[0])
   if jid in START_JID:
      #par = p.split()
      if par:
         par = par.split()
         if len(par) < 3:
            reply(t,s,u'Пиши так Подкрепление ник юнит число')
            return
         user = START_JID[jid]
         if not par[2].isdigit():
            reply(t,s,u'Укажи число')
            return
         podkrep = int(par[2])
         if par[0] in START_IGRA:
            if par[1] == u'мечник':
               zzz = mechnik
            elif par[1] == u'лучник':
               zzz = lychnik
            elif par[1] == u'рыцарь':
               zzz = ricar
            elif par[1] == u'паладин':
               zzz = paladin
            elif par[1] == u'маг':
               zzz = mag
            elif par[1] == u'джин':
               zzz = jin
            elif par[1] == u'дракон':
               zzz = dragon
            else:
               reply(t,s,u'Нет такого юнита')
               return
            if par[2].isdigit():
               
               igrok = START_IGRA[par[0]]
               if podkrep <= ARMIA[jid][zzz]:
                  ARMIA[jid][zzz] -= podkrep
                  ARMIA[igrok][zzz] += podkrep
                  with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
                  reply(t,s,u'Подкрепление игроку '+str(par[0])+u' отправлено!\n• '+str(par[1])+u': '+str(podkrep))
                  
                  msg(igrok,u'Пришло подкрепление от игрока '+str(user)+u'\n• '+str(par[1])+u': '+str(podkrep))
                  return
               else:
                  reply(t,s,u'Указанное число больше твоей армии')
                  return
            else:
               reply(t,s,u'Третий параметр должен быть числом')
               return
         else:
            reply(t,s,u'Нет такого игрока')
            return
      else:
         reply(t,s,u'аблом')

register_command_handler(podkrep, 'подкрепление', [], '10', 'отправляет подкреп другому игроку.', 'подкрепление ник юнит число', ['подкрепление Вася мечник 100'])

def load_armia(*list):
        global ARMIA
        try:
                with file('dynamic/armia.txt', 'r') as fp: ARMIA = eval(fp.read())
        except:
                ARMIA = {}
                with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))

def load_garniz(*list):
        global GARNIZ
        try:
                with file('dynamic/garniz.txt', 'r') as fp: GARNIZ = eval(fp.read())
        except:
                GARNIZ = {}
                with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))

register_stage1_init(load_armia)
register_stage1_init(load_garniz)