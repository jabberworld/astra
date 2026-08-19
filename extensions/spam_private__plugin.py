#===istalismanplugin===
# -*- coding: utf-8 -*-




def handler_kick_ass(type, source, parameters):
        if source[1] in GROUPCHATS:
                if len(parameters.split()) == 3:
                        splitdata = parameters.split()
                        rep,jid,msgnum,smlnum = '','',int(splitdata[1]),int(splitdata[2])
                        if msgnum>20000 or smlnum>20000:
                                reply(type,source,u'облом :-(')
                                return
                        reply(type,source,u'ок')
                        if splitdata[0]==u':-D':
                                for x in range(0, msgnum):
                                        for y in range(0, smlnum):
                                                rep += u''
                                        msg(source[1], rep)
                                        rep = ''
#					time.sleep(0.5)
                        else:
                                if splitdata[0].count('@'):
                                        jid=splitdata[0]
                                else:
                                        jid=source[1]+'/'+splitdata[0]
                                #print jid
                                for x in range(0, msgnum):
                                        for y in range(0, smlnum):
                                                rep += u':-*'
                                        msg(jid, rep)
                                        rep=''
#					time.sleep(0.5)
                        reply(type,source,u'ок')
                else:
                        reply(type,source,u'read "х спам"')


#  listed below command handler are not recommended
register_command_handler(handler_kick_ass, 'смайл', ['все'], 100, 'Спамит приват смайлами в текущей конференции. \nИспользование: смайл <nick> параметр.\nПовторение спама определяется вторым параметром <кол-во>.\nКоличество спама определяется третьим параметром <кол-во>.\nПисать эту команду лучше в привате.', 'смайл <nick> <кол-во> <кол-во>', ['смайл bLaDe 1000 10','смайл guy 500 8'])