# BS mark.1-55
# /* coding: utf-8 */
# Author: WithcerGeralt
# Ported from BlackSmith m.2 
# (c) simpleApps, 2011

def find_cmd(mType, source, body):
        message = ''
        if body:
                ls = body.split()
                try:
                        cmd = COMMANDS[ls[0]]
                        plug = cmd["plug"]
                        message = u"Я нашла команду %s в плагине %s"%(ls[0],plug)
                except:
                        message = u"Не найдено."
        else:
                message = u"Недостаточно параметров."
        reply(mType, source, message)

command_handler(find_cmd, 100, "find_cmd")