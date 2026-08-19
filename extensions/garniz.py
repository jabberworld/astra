#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

def garniz(t,s,p):
   jid = handler_jid(s[0])
   if not jid in GARNIZ:
      GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, paladin: 0, jin: 0, dragon: 0}
   if not p:
      if GARNIZ[jid][mechnik] > 0:
         reply(t,s,u'Защита замка:\nМечник: '+str(GARNIZ[jid][mechnik]))
         return
      if GARNIZ[jid][lychnik] > 0:
         reply(t,s,u'Защита замка:\nЛучник: '+str(GARNIZ[jid][lychnik]))
         return
      if GARNIZ[jid][ricar] > 0:
         reply(t,s,u'Защита замка:\nРыцарь: '+str(GARNIZ[jid][ricar]))
         return
      if GARNIZ[jid][paladin] > 0:
         reply(t,s,u'Защита замка:\nПаладин: '+str(GARNIZ[jid][paladin]))
         return
      else:
         reply(t,s,u'Гарнизон пуст')
         return
   if p in [u'распустить']:
      if GARNIZ[jid][mechnik] > 0:
         ARMIA[jid][mechnik] += GARNIZ[jid][mechnik]
         GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         
         reply(t,s,u'Гарнизон распущен')
         return
      if GARNIZ[jid][lychnik] > 0:
         ARMIA[jid][lychnik] += GARNIZ[jid][lychnik]
         GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         
         reply(t,s,u'Гарнизон распущен')
         return
      if GARNIZ[jid][ricar] > 0:
         ARMIA[jid][ricar] += GARNIZ[jid][ricar]
         GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         
         reply(t,s,u'Гарнизон распущен')
         return
      if GARNIZ[jid][paladin] > 0:
         ARMIA[jid][paladin] += GARNIZ[jid][paladin]
         GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
         with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
         with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
         
         reply(t,s,u'Гарнизон распущен')
         return
   else:
      p = p.split()
      name_unit = p[0]
      col_unit = int(p[1])
      if name_unit in [u'мечник']:
         if col_unit < ARMIA[jid][mechnik]:
            if GARNIZ[jid][lychnik] > 0:
               ARMIA[jid][lychnik] += GARNIZ[jid][lychnik]
               GARNIZ[jid][lychnik] = 0
            if GARNIZ[jid][ricar] > 0:
               ARMIA[jid][ricar] += GARNIZ[jid][ricar]
               GARNIZ[jid][ricar] = 0
            if GARNIZ[jid][paladin] > 0:
               ARMIA[jid][paladin] += GARNIZ[jid][paladin]
               GARNIZ[jid][paladin] = 0
            #GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
            GARNIZ[jid][mechnik] += col_unit
            ARMIA[jid][mechnik] -= col_unit
            with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
            with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
            reply(t,s,u'Гарнизон создан!\nМечники: +'+str(col_unit))
            return
         else:
            reply(t,s,u'Указанное число больше твоей армии')
            return
      if name_unit in [u'лучник']:
         if col_unit < ARMIA[jid][lychnik]:
            if GARNIZ[jid][mechnik] > 0:
               ARMIA[jid][mechnik] += GARNIZ[jid][mechnik]
               GARNIZ[jid][mechnik] = 0
            if GARNIZ[jid][ricar] > 0:
               ARMIA[jid][ricar] += GARNIZ[jid][ricar]
               GARNIZ[jid][ricar] = 0
            if GARNIZ[jid][paladin] > 0:
               ARMIA[jid][paladin] += GARNIZ[jid][paladin]
               GARNIZ[jid][paladin] = 0
            #GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
            GARNIZ[jid][lychnik] += col_unit
            ARMIA[jid][lychnik] -= col_unit
            with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
            with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
            reply(t,s,u'Гарнизон создан!\nЛучники: +'+str(col_unit))
            return
         else:
            reply(t,s,u'Указанное число больше твоей армии')
            return
      if name_unit in [u'рыцарь']:
         if col_unit < ARMIA[jid][ricar]:
            if GARNIZ[jid][lychnik] > 0:
               ARMIA[jid][lychnik] += GARNIZ[jid][lychnik]
               GARNIZ[jid][lychnik] = 0
            if GARNIZ[jid][mechnik] > 0:
               ARMIA[jid][mechnik] += GARNIZ[jid][mechnik]
               GARNIZ[jid][mechnik] = 0
            if GARNIZ[jid][paladin] > 0:
               ARMIA[jid][paladin] += GARNIZ[jid][paladin]
               GARNIZ[jid][paladin] = 0
            #GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
            GARNIZ[jid][ricar] += col_unit
            ARMIA[jid][ricar] -= col_unit
            with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
            with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
            reply(t,s,u'Гарнизон создан!\nРыцари: +'+str(col_unit))
            return
         else:
            reply(t,s,u'Указанное число больше твоей армии')
            return
      if name_unit in [u'паладин']:
         if col_unit < ARMIA[jid][paladin]:
            if GARNIZ[jid][lychnik] > 0:
               ARMIA[jid][lychnik] += GARNIZ[jid][lychnik]
               GARNIZ[jid][lychnik] = 0
            if GARNIZ[jid][mechnik] > 0:
               ARMIA[jid][mechnik] += GARNIZ[jid][mechnik]
               GARNIZ[jid][mechnik] = 0
            if GARNIZ[jid][ricar] > 0:
               ARMIA[jid][ricar] += GARNIZ[jid][ricar]
               GARNIZ[jid][ricar] = 0
            #GARNIZ[jid] = {mechnik: 0, ricar: 0, mag: 0, lychnik: 0, razved: 0, paladin: 0, jin: 0, dragon: 0}
            GARNIZ[jid][paladin] += col_unit
            ARMIA[jid][paladin] -= col_unit
            with file('dynamic/armia.txt', 'w') as fp: fp.write(str(ARMIA))
            with file('dynamic/garniz.txt', 'w') as fp: fp.write(str(GARNIZ))
            reply(t,s,u'Гарнизон создан!\nРыцари: +'+str(col_unit))
            return
         else:
            reply(t,s,u'Указанное число больше твоей армии')
            return

register_command_handler(garniz, 'гарнизон', [], 10, 'Добавление, удаление, замена армии в защитном гарнизоне замка', 'гарнизон параметр', ['гарнизон мечник 100, гарнизон распустить, гарнизон'])
