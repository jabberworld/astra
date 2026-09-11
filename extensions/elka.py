#===istalismanplugin===
# -*- coding: utf-8 -*-
# ★
E_CON = {}
ELKA = {}
E_SH = {}

def elka1(type, source, body):
   if body == u'посмотреть':
      if source[1] in E_CON.keys():
         reply(type,source,str(ELKA[source[1]]))
         return
      else:
         reply(type, source, u'на что смотреть собралсо?')
         return
   if body == u'установить':
      if source[1] in A_TOPIC.keys():
         if source[1] not in E_CON.keys():
            E_CON[source[1]] = 1
            ELKA[source[1]] = r'''.
            ¨¨¨¨¨¨¨¨¨¨*
            ¨¨¨¨¨¨¨¨¨***
            ¨¨¨¨¨¨¨¨*****
            ¨¨¨¨¨¨¨*******
            ¨¨¨¨¨¨*********
            ¨¨¨¨¨***********
            ¨¨¨¨*************
            ¨¨¨***************
            ¨¨*****************
            ¨*******************
            *********************
            ¨¨¨¨¨____!_!____ ¨¨¨¨
            ¨¨¨¨¨\_________/¨¨¨¨¨¨'''
            JCON.send(xmpp.Message(unicode(source[1]), "", "groupchat", str.join('',A_TOPIC[source[1]])+'\n'+str(ELKA[source[1]])))
            return
         else:
            reply(type,source,u'Уже установлено! Но как вариант попробуйте убрать а потом опять установить.')
            return
      else:
         reply(type, source, u'Для начала сохраните вашу тему, через команду АТОПИК* текст_темы')
         return
   if body == u'убрать':
      if source[1] in A_TOPIC.keys():
         if source[1] in E_CON.keys():
            JCON.send(xmpp.Message(unicode(source[1]), "", "groupchat", str.join('',A_TOPIC[source[1]])))
            del E_CON[source[1]]
            return
         else:
            JCON.send(xmpp.Message(unicode(source[1]), "", "groupchat", str.join('',A_TOPIC[source[1]])))
            return
      else:
         reply(type,source,u'не установлено')
         return
   if body == u'нарядить':
      if source[1] in A_TOPIC.keys():
         if source[1] in E_CON.keys():
            if source[1] not in E_SH.keys():
               E_SH[source[1]] = 1
            if source[1] in A_C_T.keys():
               ELKA[source[1]] = r'''.
               ¨¨¨¨¨¨¨¨¨★
               ¨¨¨¨¨¨¨¨¨**
               ¨¨¨¨¨¨¨¨¨*o*
               ¨¨¨¨¨¨¨¨*♥*o*
               ¨¨¨¨¨¨¨***o***
               ¨¨¨¨¨¨**o**♥*o*
               ¨¨¨¨¨**♥**o**o**
               ¨¨¨¨**o**♥***♥*o*
               ¨¨¨*****♥*o**o****
               ¨¨**♥**o*****o**♥**
               ¨******o*****♥**o***
               ****o***♥**o***o***♥*
               ¨¨¨¨¨____!_!____
               ¨¨¨¨¨\_________/¨¨¨¨¨¨¨'''
               JCON.send(xmpp.Message(unicode(source[1]), "", "groupchat", str.join('',A_TOPIC[source[1]])+'\n'+str(ELKA[source[1]])))
               return
            else:
               reply(type,source,u'Наряжай сам!')
               return
         else:
            reply(type,source,u'Не установлено.')
      else:
         reply(type,source,u'Не установлено.')
         return
   else:
      reply(type,source,u'Ну ёлка и что дальше?')


register_command_handler(elka1, 'ёлка', [], 30, 'Добавляет в тему конференции новогоднюю елку. Доступные параметры: установить - добавление ёлки, убрать - убирает ёлку, нарядить - если запущен тамагочик, то наряжает ёлку, посмотреть - просто показывает ёлку.', 'ёлка параметр', ['ёлка установить'])