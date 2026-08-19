#===istalismanplugin===
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  auto_turn_plugin.py
#  Ver.5.1

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

RUSIMBOLS = 'а/б/в/г/д/е/ё/ж/з/и/й/к/л/м/н/о/п/р/с/т/у/ф/х/ц/ч/ы/ъ/ь/ш/щ/э/ю/я/№'

from base64 import b64encode

def check_nosimbols(item):
   item = item.lower()
   for simbol in RUSIMBOLS.split('/'):
      if item.count(simbol):
         return False
   return True

en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,.Ю`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>Б~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,.ю`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>б~"))
OBSCENE2 = u'бляд/ блят/ бля / блять / плять /хуй/ ибал/ ебал/ хуи/хуител/хуя/ хую/ хуе/ ахуе/ охуе/хуев/ хер /хер/ пох / нах /писд/пизд/рizd/ пздц / еб/ епана / епать / ипать / выепать / ибаш/ уеб/проеб/праеб/приеб/съеб/взъеб/взьеб/въеб/вьеб/выебан/перееб/недоеб/долбоеб/долбаеб/ ниибац/ неебац/ неебат/ ниибат/ пидар/ рidаr/ пидар/ пидор/педор/пидор/пидарас/пидараз/ педар/педри/пидри/ заеп/ заип/ заеб/ебучий/ебучка /епучий/епучка / заиба/заебан/заебис/ выеб/выебан/ поеб/ наеб/ наеб/сьеб/взьеб/вьеб/ гандон/ гондон/пахуи/похуис/ манда /мандав/залупа/ залупог'
SMILES = u''':4*4(4)4[4]'''
SLOVO3 = u'''disc/took/love/privet/hello/hi/kak/dela/VERSION/version/ping/vcard/command/commands/botup/pomogi/pochemy/how/are/you/name/posoni/work/rabota/and/would/them/down/think/come/then/where/like/into/back/will/see/no/one/know/all/my/look/was/has/from/this/get/out/they/him/can/cat/but/her/for/say/she/with/his/that/have/help/info/O_o/BOSS/boss/how'''

ATURN = {}

def check_obscene_words(body):
        body = ' %s ' % body.lower()
        for item in OBSCENE2.split('/'):
                if body.count(item):
                        return True
        return False

def check_words_base(body):
        body = ' %s ' % body.lower()
        for item in SLOVO3.split('/'):
                if body.count(item):
                        return True
        return False

def check_smiles_words(body):
#	body = ' %s ' % body.lower()
        for item in SMILES.split('4'):
                if body.count(item):
                        return True
                else:
                         for item in SMILE1:
                                  if body.count(item):
                                           return True
        return False

def check_base_words(body):
        body = ' %s ' % body.lower()
        for item in ATURN_BASE:
                if body.count(item):
                        return True
        return False

def func_rebody2(body, list):
        for x in list:
                body = body.replace(x, '')
        return body.strip()

def handler_aturn(raw, type, source, body):
        if type == 'public' and source[2] != '':
                if ATURN[source[1]] != 'off':
                        list = {}
                        for nick in GROUPCHATS[source[1]].keys():
                                if GROUPCHATS[source[1]][nick]['ishere']:
                                        for key in [nick+key for key in [':',',','>']]:
                                                if body.count(key):
                                                        col = '*%s*' % str(len(list.keys()) + 1)
                                                        list[col] = key
                                                        body = body.replace(key, col)
                                if body.count(nick):
                                        col2 = '*%s*' % str(len(list.keys()) + 1)
                                        list[col2] = nick
                                        body = body.replace(nick, col2)
                        if check_nosimbols(body) and len(body) < 52:
                                  rebody2 = func_rebody2(body, list.keys())
                                  if rebody2 and not check_number(rebody2):
                                           if not check_base_words(rebody2):
                                                    if not check_words_base(rebody2):
                                                             if check_smiles_words(rebody2):
                                                                      for i in SMILES.split('4'):
                                                                               return
                                                                               #body = body.replace(i,'')
                                                                               #rebody1 = body
                                                                               #smile = i
                                                                               #if len(rebody1) > 0:
                                                                                        
                                                                                        #rebody = reduce(lambda x,y: en2ru_table.get(x,x)+en2ru_table.get(y,y), rebody1)
                                                                               #else:
                                                                               
                                                                                        #return
                                                                      else:
                                                                               for i in SMILE1:
                                                                                        #body = body.replace(i,'')
                                                                                        #rebody1 = body
                                                                                        #smile = i
                                                                                        #if len(rebody1) > 0:
                                                                                                 #rebody = reduce(lambda x,y: en2ru_table.get(x,x)+en2ru_table.get(y,y), rebody1)
                                                                                        #else:
                                                                                        return
                                                             else:
                                                                      #smile = ''
                                                                       rebody = ''.join(en2ru_table.get(x, x) for x in body)
                                                             if not check_obscene_words(rebody):
                                                                      for x in list:
                                                                               rebody = rebody.replace(x, list[x])
                                                                      msg(source[1], u'расшифровала записи на глиняных табличках:\n %s, %s' % (source[2], rebody))
                                                             else:
                                                                      reply(type, source, u'хрена ругаешся!?')


def handler_aturn_control(type, source, body):
        if source[1] in GROUPCHATS:
                if body:
                        body = body.lower()
                        filename = 'dynamic/'+source[1]+'/aturn.txt'
                        if body in [u'вкл', 'on', '1']:
                                ATURN[source[1]] = 'on'
                                write_file(filename, "'on'")
                                reply(type, source, u'авто-турн включен')
                        elif body in [u'выкл', 'off', '0']:
                                ATURN[source[1]] = 'off'
                                write_file(filename, "'off'")
                                reply(type, source, u'авто-турн выключен')
                        else:
                                reply(type, source, u'читай помощь по команде')
                else:
                        if ATURN[source[1]] == 'off':
                                reply(type, source, u'сейчас авто-turn выключен')
                        else:
                                reply(type, source, u'сейчас авто-turn включен')
        else:
                reply(type, source, u'только в чате мудак!')

def aturn_init(conf):
        if check_file(conf, 'aturn.txt', "'on'"):
                state = eval(read_file('dynamic/'+conf+'/aturn.txt'))
        else:
                state = 'on'
                delivery(u'Внимание! Не удалось создать aturn.txt для "%s"!' % (conf))
        ATURN[conf] = state

ATURN_BASE = []
SMILE1 = []

def aturnsmileadd(type, source, slovo):
   if not slovo:
      reply(type,source,u'База исключения смайлов атурна: '+str.join(' • ',SMILE1))
      return
   else:
      SMILE1.append(slovo)
      aturnsmile_save_now()
      reply(type,source,u'ok')

register_command_handler(aturnsmileadd, 'смайл+', [], 100, '', '', [''])

def aturnsmile_load_now(*list):
        global SMILE1
        try:
                fp = file('dynamic/aturnsmile.txt', 'r')
                SMILE1 = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/aturnsmile.txt', 'w')
                SMILE1 = []
                fp.write( str(SMILE1) )
                fp.close()

def aturnsmile_save_now():
        global SMILE1
        fp = file('dynamic/aturnsmile.txt', 'w')
        fp.write( str(SMILE1) )
        fp.close()

register_stage1_init(aturnsmile_load_now)

def aturnadd(type, source, slovo):
   if not slovo:
      reply(type,source,u'База исключения атурна: '+str.join(' • ',ATURN_BASE))
      return
   else:
      ATURN_BASE.append(slovo)
      aturnbase_save_now()
      reply(type,source,u'ok')

register_command_handler(aturnadd, 'атурн+', [], 100, '', '', [''])

def aturnbase_load_now(*list):
        global ATURN_BASE
        try:
                fp = file('dynamic/aturnbase.txt', 'r')
                ATURN_BASE = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/aturnbase.txt', 'w')
                ATURN_BASE = []
                fp.write( str(ATURN_BASE) )
                fp.close()

def aturnbase_save_now():
        global ATURN_BASE
        fp = file('dynamic/aturnbase.txt', 'w')
        fp.write( str(ATURN_BASE) )
        fp.close()

register_stage1_init(aturnbase_load_now)
register_message_handler(handler_aturn)
register_command_handler(handler_aturn_control, 'атурн', ['все','разное'], 20, 'Включение/выключение авто-турна, без параметра покажет текущее состояние\nBy WitcherGeralt\nhttp://witcher-team.ucoz.ru/', 'атурн [вкл/on/1/выкл/off/0]', ['атурн вкл','атурн выкл'])

register_stage1_init(aturn_init)
