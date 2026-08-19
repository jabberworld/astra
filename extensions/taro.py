#===istalismanplugin===
# -*- coding: utf-8 -*-

TARO_C = {}
TARO_HELP = u'• 1 - Гадание на одну карту (СОВЕТ).\nЭто гадание блестяще оправдывает себя, когда нужен альтернативный ответ, да или нет, на точный и конкретный вопрос. Тут же дается толкование. К достоинствам подобных методов гадания относится их быстрота и доступность. При гадании прочитывается суть ситуации. \n• 2 - Линия времени\nЭтот расклад основан на представлении о том, что прошлое формирует настоящее, и настоящее формирует будущее.'

def menu_taro(t,s,p):
   if t == 'private':
      reply(t,s,u'Только в чате!')
      return
   if s[1] not in TARO_C:
      TARO_C[s[1]] = 1
      mes = u'Меню Раскладов таро:'
      register_command_handler(rasklad1, '1', [], 10, '', '', [''])
      register_command_handler(rasklad2, '2', [], 10, '', '', [''])
      register_command_handler(taro_help, '3', [], 10, '', '', [''])
      register_command_handler(taro_menu_ex, '0', [], 10, '', '', [''])
      mes += u'\n• 1 - Совет.'
      mes += u'\n• 2 - Линия времени.'
      mes += u'\n• 3 - Помощь.'
      mes += u'\n• 0 - Выход.'
      reply(t,s,mes)
      time.sleep(300)
      if s[1] in TARO_C:
         taro_menu_ex(t,s,p)
      else:
         return
   else:
      reply(t,s,u'Расклады и так открыты! Отправь цифру (номер расклада)')

register_command_handler(menu_taro, 'таро', [], 10, 'Рассклады на картах Таро', 'таро', ['таро'])

def rasklad1(t,s,p):
   stol = u'''
   ⌈ ︸ ⌉
  【 '|' 】
   ⌊ ︷ ⌋ '''
   reply(t,s,stol+u'\nСовет, расклад на одну карту.')
   msg(s[1], u'/me Взяла карты и тасует колоду...')
   time.sleep(3)
   reply(t,s,u'Пока я тасую колоду, подумайте еще раз о своем вопросе.')
   time.sleep(60)
   TARO = eval(read_file('static/taro.txt'))
   time.sleep(3)
   mk = [u'Прямая:\n',u'Перевернутая:\n']
   mes = random.choice(mk)
   mes += random.choice(TARO)
   reply(t,s,mes)

def rasklad2(t,s,p):
   stol = u'''
   ⌈ ︸ ⌉   ⌈ ︸ ⌉   ⌈ ︸ ⌉
  【 '|' 】 【 '|' 】 【 '|' 】
   ⌊ ︷ ⌋   ⌊ ︷ ⌋   ⌊ ︷ ⌋ '''
   reply(t,s,stol+u'\nРасклад на три карты.')
   msg(s[1], u'/me Взяла карты и тасует колоду...')
   time.sleep(3)
   reply(t,s,u'Пока я тасую колоду, подумайте еще раз о своем вопросе.')
   time.sleep(40)
   TARO = eval(read_file('static/taro.txt'))
   mk = [u'Прямая:\n',u'Перевернутая:\n']
   mes = random.choice(mk)
   mes += random.choice(TARO)
   mes1 = random.choice(mk)
   mes1 += random.choice(TARO)
   mes2 = random.choice(mk)
   mes2 += random.choice(TARO)
   
   msg(s[1],u'/me '+mes)
   time.sleep(30)
   msg(s[1],u'/me '+mes1)
   time.sleep(30)
   msg(s[1],u'/me '+mes2)

def taro_help(t,s,p):
   reply(t,s,TARO_HELP)

def taro_menu_ex(t,s,p):
   handler_command_out1(t, s, '1')
   handler_command_out1(t, s, '2')
   handler_command_out1(t, s, '3')
   handler_command_out1(t, s, '0')
   del TARO_C[s[1]]
   reply(t,s,u'Спрятала карты...')
