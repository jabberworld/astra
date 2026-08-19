#===istalismanplugin===
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  qipstatus_plugin.py

# Coded by Denizo


def handler_qstat(type,source,parameters):
        qipfr = read_file('static/status.txt').split('\n')
        reply(type, source, (random.choice(qipfr)))
        


register_command_handler(handler_qstat, 'статусы', ['все'], 10, 'показывает статусное сообщение из сборника прикольных статусов', 'статусы', ['статусы'])
