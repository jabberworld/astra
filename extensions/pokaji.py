#===istalismanplugin===
# -*- coding: utf-8 -*-

def pokaji(type, source, p):
   if p == u'пинг':
      if len(p) == 2:
         nick = p[2]
         handler_ping(type,source,nick)
      else:
         nick = source[0]
         handler_ping(type,source,nick)


#register_command_handler(pokaji, 'покажи', [], 0, '', '', [''])