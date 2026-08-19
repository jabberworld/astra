#===istalismanplugin===
# ~*~ coding: utf-8 ~*~

MONEY = {}

def bandit(t,s,p):
   global MONEY
   jid = handler_jid(s[0])
   if p == u'заново':
      del MONEY[jid]
   stavka = 5
   if p.isdigit() and int(p) in range(1,11):
      stavka = p
   if not jid in MONEY:
      MONEY[jid] = 100
   if MONEY[jid] < 0:
      reply(t,s,u'Нет средств, начните игру заново (командуй бандит заново)')
      return
   reply(t,s,u'Твой счет: '+str(MONEY[jid])+u'$\nСтавка: '+str(stavka)+u'$\nНачинаем :)')
   MONEY[jid] -= int(stavka)
   time.sleep(3)
   repl = ''
   for x in range(3):
      st = (u'первой', u'второй', u'третьей')[x]
      mes = ['®','&','¢','£','€','¥','@']
      mis1 = random.choice(mes)
      mis2 = random.choice(mes)
      mis3 = random.choice(mes)
      msg(s[1],u'/me [ '+mis1+' ]'+'[ '+mis2+' ]'+'[ '+mis3+' ]')
      time.sleep(1)
      if mis1 == mis2 == mis3:
         MONEY[jid] += int(stavka) * 26
         repl += u'\nВыигрыш %s строки! %sх25\nДжек пот!!!' % (st, str(stavka))
      if mis1 != mis2 == mis3:
         MONEY[jid] += int(stavka) * 3
         repl += u'\nВыигрыш %s строки! %sх2' % (st, str(stavka))
      if mis1 == mis2 != mis3:
         MONEY[jid] += int(stavka) * 6
         repl += u'\nВыигрыш %s строки! %sх5' % (st, str(stavka))
   repl += u'\nТвой остаток на счете: '+str(MONEY[jid])+'$'
   time.sleep(3)
   with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))
   reply(t, s, repl)

def load_bandit(*list):
        global MONEY
        try:
                with file('dynamic/money.txt', 'r') as fp: MONEY = eval(fp.read())
        except:
                MONEY = {}
                with file('dynamic/money.txt', 'w') as fp: fp.write(str(MONEY))

register_stage1_init(load_bandit)

register_command_handler(bandit, 'бандит', [], 10, 'Игра однорукий бандит.\nСтавка определяется параметром, число 1-10', 'бандит', ['бандит 7'])