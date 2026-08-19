#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploru.net>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_pulemet(type, source, parameters):
        if type=='private':
            reply(type,source,u'только в чате')
        nicks = GROUPCHATS[source[1]].keys()
        if parameters in nicks:
                replies = [u'Тррраа-та-та-та-т-та-та-т-ат', u'Пдщь!', u'Трр-трт-р-т-рр-т--рт-рт', u'Пыхх!', u'Трам-тарам!', u'Бах!', u'ТРАТАТАТАТАТАААААХХХХ!!!!!!!!!']
                rep = random.choice(replies)
                msg(source[1], parameters+': '+rep)
                node=xmpp.simplexml.XML2Node(unicode("<iq id='266' to='" +source[1]+ "' type='set' xml:lang='ru'><query xmlns='http://jabber.org/protocol/muc#admin'><item nick='"  +parameters+ "' role='none'/></query></iq>").encode('utf8'))
                JCON.send(node)
                if source[1] not in POL_SEX.keys():
                         reply(type, source, u'Разрешетила его!')
                else:
                          reply(type, source, u'Разрешетил его!')
                

register_command_handler(handler_pulemet, 'пулемёт', ['все','админ'], 10, 'Расстрелять всех нах.. ', 'пулемёт', ['пулемёт nick'])
