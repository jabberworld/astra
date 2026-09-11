#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

def razvedka(t,s,par):
   jid = handler_jid(s[0])
   if jid in START_JID:
      if RAZVED_COL[jid] >=5:
         if par in START_IGRA:
            p = START_IGRA[par]
            if RAZVED_COL[jid] > 4 and RAZVED_COL[jid] < 10:
               if ARMIA[jid][razved] > ARMIA[p][razved]:
                  msg(jid,u'Разведка игрока '+par+u'\n•••Ресурсы:\n• Дерево: '+str(WOOD[p])+u'\n• Камень: '+str(STONE[p])+u'\n• Железо: '+str(IRON[p])+u'\n• Еда: '+str(EAT[p]))
                  reply(t,s,u'Разведка игрока '+par+u'\n•••Ресурсы:\n• Дерево: '+str(WOOD[p])+u'\n• Камень: '+str(STONE[p])+u'\n• Железо: '+str(IRON[p])+u'\n• Еда: '+str(EAT[p]))
                  return
                  
               else:
                  reply(t,s,u'У '+par+u' больше разведчиков чем у тебя! Твоим Шпионам пришлось бежать и к сожалению им не удалось украсть информацию')
                  
                  return
            if RAZVED_COL[jid] >= 10:
               if ARMIA[jid][razved] > ARMIA[p][razved]:
                  reply(t,s,u'Разведка игрока '+par+u'\n•••Ресурсы:\n• Дерево: '+str(WOOD[p])+u'\n• Камень: '+str(STONE[p])+u'\n• Железо: '+str(IRON[p])+u'\n• Еда: '+str(EAT[p])+u'\n••• Защита замка:\n• Мечников '+str(GARNIZ[p][mechnik])+u'\n• Лучников '+str(GARNIZ[p][lychnik])+u'\n• Рыцари '+str(GARNIZ[p][ricar])+u'\n• Маги '+str(GARNIZ[p][mag])+u'\n• Паладины '+str(GARNIZ[p][paladin])+u'\n• Джины '+str(GARNIZ[p][jin])+u'\n• Драконы '+str(GARNIZ[p][dragon]))
                  return
               else:
                  reply(t,s,u'У '+par+u' больше разведчиков чем у тебя! Твоим Шпионам пришлось бежать и к сожалению им не удалось украсть информацию')
                  return
            
            else:
               reply(t,s,u'Построй корпус 5 уровня')
               return
         else:
            reply(t,s,u'Игрок не найден.')
            return
      else:
         reply(t,s,u'Построй корпус хотя бы 5 уровня')
         return
   else:
      reply(t,s,u'Начни играть')

register_command_handler(razvedka, 'разведка', [], 10, '', '', [''])
