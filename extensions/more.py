#===istalismanplugin===
# /* coding: utf-8 */

#  BlackSmith plugin
#  more_plugin.py

#  Initial Copyright © 2009 Als [als-als@ya.ru]
#  Modifications: WitcherGeralt [WitcherGeralt@rocketmail.com]

MORE = {}

def handler_more(type, source, body):
        if type == 'public' and source[1] in MORE:
                if MORE[source[1]]:
                        reply(type, source, MORE[source[1]])

def handler_more_outmsg(target, body, obody):
        if target in MORE:
                if hash(obody) != MORE[target]:
                        if len(obody) > CHAT_MSG_LIMIT:
                                MORE[target] = obody[CHAT_MSG_LIMIT:]

def init_more(conf):
        MORE[conf] = None

register_outgoing_message_handler(handler_more_outmsg)
command_handler(handler_more, 10, "more")

register_stage1_init(init_more)
