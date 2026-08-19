#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  access_plugin.py
#  updated by Gigabyte
#  mail: gigabyte@ngs.ru

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

ACCESS_NAME = {}


def handler_access_view_access(type, source, parameters):
        accdesc={'-100':'(полный игнор)','-1':'(заблокирован)','0':'(никто)','1':'(лол)','10':'(♟)','11':'(♟)','15':'(♞)','16':'(♞)','20':'(♝)','30':'(♜)','80':'(♚)','100':'(♚)'}

        if parameters==u'инфо':
                if type == 'public':
                    reply(type,source,u'Глянь в привате')
                reply('private',source,u'-100 - полный игнор, все сообщения от юзера с таким доступом будут пропускатся на уровне ядра\n-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается визиторам (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается партисипантам (participant)\n11 - расширенный набор команд и макросов (например доступ к !!!), автоматически присваивается мемберам (member)\n15 (16) - модераторский набор команд и макросов, автоматически присваевается модераторам (moderator)\n20 - админский набор команд и макросов, автоматически присваивается админам (admin)\n30 - овнерский набор команд и макросов, автоматически присваиватся овнерам (owner)\n80 - позволяет юзеру с этим доступом заводить и выводить бота из конференций\n100 - администратор бота, может всё')
                return
        if not parameters:
                level=str(user_level(source[1]+'/'+source[2], source[1]))
                if level in accdesc.keys():
                        levdesc=accdesc[level]
                else:
                        levdesc=''
                if handler_jid(source[0]) in ACCESS_NAME:
                        if level in ACCESS_NAME[ handler_jid(source[0]) ]:
                                levdesc = '(%s)' % ACCESS_NAME[ handler_jid(source[0]) ][ level ]
                reply(type, source, level+' '+levdesc)
        else:
                nicks = GROUPCHATS[source[1]].keys()
                if parameters.strip() in nicks:
                        level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
                        if level in accdesc.keys():
                                levdesc=accdesc[level]
                        else:
                                levdesc=''
                                
                        if handler_jid(source[1]+'/'+parameters.strip()) in ACCESS_NAME:
                                if level in ACCESS_NAME[ handler_jid(source[1]+'/'+parameters.strip()) ]:
                                        levdesc = '(%s)' % ( ACCESS_NAME[ handler_jid(source[1]+'/'+parameters.strip() ) ][ level ] )

                        reply(type, source, level+' '+levdesc)
                else:
                        reply(type, source, u'а он тут? :-O')

def handler_access_name(t, s, p):
        global ACCESS_NAME
        if not handler_jid(s[0]) in ACCESS_NAME.keys():
                ACCESS_NAME[ handler_jid(s[0]) ] = {}
        p = p.split(':', 1)
        if len(p)==2:
                try:
                        a = int(p[0])
                except:
                        reply(t, s, u'Доступ должен быть числом')
                        return
                if p[1]=='':
                        reply(t, s, u'Укажи описание')
                        return
                ACCESS_NAME[ handler_jid(s[0]) ][ p[0] ] = p[1]
                reply(t, s, u'Добавлено')
                access_save_now()
        else:
                reply(t, s, u'Пиши так: ДОСТУП:ОПИСАНИЕ')

def access_load_now(*list):
        global ACCESS_NAME
        try:
                fp = file('dynamic/accname.txt', 'r')
                ACCESS_NAME = eval( fp.read() )
                fp.close()
        except:
                fp = file('dynamic/accname.txt', 'w')
                ACCESS_NAME = {}
                fp.write( str(ACCESS_NAME) )
                fp.close()

def access_save_now():
        global ACCESS_NAME
        fp = file('dynamic/accname.txt', 'w')
        fp.write( str(ACCESS_NAME) )
        fp.close()

register_stage1_init(access_load_now)
register_command_handler(handler_access_name, 'access', ['доступ','все'], 0, 'Команда находится в плагине:\naccess_plugin.py\nПоменять описание доступа для себя. Например когда вы пишите "доступ" и бот отвечает 10 - постоянный участник, если вам этот текст не нравиться вы можете этой командой его поменять', 'access ДОСТУП:ОПИСАНИЕ', ['access 20:Комнатный домовой'])
register_command_handler(handler_access_view_access, 'доступ', ['доступ','админ','все'], 10, 'Команда находится в плагине:\naccess_plugin.py\nПоказывает уровень доступа определённого ника.\nПодробнее о стандартных уровнях доступа - напиишите "доступ инфо".', 'доступ [ник]', ['доступ', 'доступ guy'])

