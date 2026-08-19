#===istalismanplugin===
# -*- coding: utf-8 -*-

import smtplib
import os

from email.mime.text import MIMEText


        
gmail_user = 'kantyzeni@bk.ru'
gmail_password = 'mwaapajj'

        # главная функция принимающая 3 параметра
        # адресат, тему письма, само сообщение 
def mail(to, subject, text):

# инициализируем наши данные
   msg = MIMEText(text, "", "windows-1251")
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

# инициализируем smtp сервер и отправляем письмо
   mailServer = smtplib.SMTP("smtp-18.1gb.ru")
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_password)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   mailServer.close()

   

mailsp=[]
def handler_email(type,source,parameters):
        groupchat=source[1]
        nick=source[2]
        jidsource=groupchat+'/'+nick
        realjid=handler_jid(jidsource)
        if groupchat == realjid:
                groupchat=u'нет'
        #level=int(user_level(jidsource, groupchat))
        #if level < 40:
        #	reply(type, source, u'недостаточно прав')
        #	return
        if type == 'public':
                reply(type, source, u'команда выполняется только в привате!')
                return
        #reply('private', source, u'мыло получено ' + mail)
        mailsp = parameters.split('&')
        #reply('private', source, mailsp[2])
        strok = u'\n ------------------------------------------------------------------------------------------- \n Отправлено при помощи бота Talisman ' + u'\n Пользователь: ' + realjid + u'\n Конференция: ' + groupchat + u'\n Внимание! Не отвечайте на данное электронное письмо!'
        mailsp[2] = mailsp[2] + strok
        mailsp[1] = mailsp[1].encode('windows-1251')
        mailsp[2] = mailsp[2].encode('windows-1251')
        mail(mailsp[0],mailsp[1],mailsp[2])
        reply(type, source, u'Отправила!')
        
        
register_command_handler(handler_email, 'email', ['суперадмин','мук','все'], 80, 'Отправка письма на мыло.(тестирование) ЗЫ: имейте ввиду в отправленном письме будет содержаться название конференции и ваш jid', 'email мыло&тема&мессага', ['email test@mail.ru&Это я!&Как у тебя дела?'])
        