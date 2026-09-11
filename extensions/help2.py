# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  help_plugin.py

# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def command_comlist2(type, source, body):
        acc100, acc80, acc30, acc20, acc15, acc10 = [], [], [], [], [], []
        if source[1] in PREFIX:
                pfx = u' (Командный префикс - "'+PREFIX[source[1]]+'"):'
        else:
                pfx = ':'
        for cmd in COMMANDS:
                if COMMANDS[cmd]['access'] == 100:
                        acc100.append(cmd)
                elif COMMANDS[cmd]['access'] == 80:
                        acc80.append(cmd)
                elif COMMANDS[cmd]['access'] == 30:
                        acc30.append(cmd)
                elif COMMANDS[cmd]['access'] == 20:
                        acc20.append(cmd)
                elif COMMANDS[cmd]['access'] == 15:
                        acc15.append(cmd)
                elif COMMANDS[cmd]['access'] == 10:
                        acc10.append(cmd)
        superadmins = u'\n\n### Команды для Суперадмина (доступ 100) - '+str(len(acc100)+len(acc80)+len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
        chiefs = u'\n\n### Команды для Глоб.Админа (доступ 80) - '+str(len(acc80)+len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
        owners = u'\n\n### Команды  для Владельцев (доступ 30) - '+str(len(acc30)+len(acc20)+len(acc15)+len(acc10))+':\n'
        admins = u'\n\n### Команды для Админов (доступ 20) - '+str(len(acc20)+len(acc15)+len(acc10))+':\n'
        moders = u'\n\n### Команды для Модеров (доступ 15) - '+str(len(acc15)+len(acc10))+':\n'
        users = u'\n\n### Команды для Участников (доступ 10) - '+str(len(acc10))+':\n'
        level = u'\n\n### Твой уровень  доступа: '
        access = user_level(source[0], source[1])
        if access == 100:
                level += u'100 (BOSS) - тебе доступны все команды'
        elif access == 80:
                level += u'80 (Chief) - тебе доступны все команды кроме суперадминских'
        elif access == 30:
                level += u'30 (Овнер) - вам доступны все команды с доступом до 30 (включительно)'
        elif access == 20:
                level += u'20 (Админ) - вам доступны команды с доступом до 20 (включительно)'
        elif access == 15 or access == 16:
                level += u'15 (Модер) - вам доступны команды для участников + пара модерских'
        elif access == 10 or access == 11:
                level += u'10 (Участник) - вам доступны команды только низшего уровня доступа (10)'
        else:
                level += u'%s - нестандартный доступ, я *dntknw* на что ты способен' % str(access)
        acc100.sort(), acc80.sort(), acc30.sort(), acc20.sort(), acc15.sort(), acc10.sort()
        boss, friend, owner, admin, moder, user = ' ♚ '.join(acc100), ' ♚ '.join(acc80), ' ♜ '.join(acc30), ' ♝ '.join(acc20), ' ♞ '.join(acc15), ' ♟ '.join(acc10)
#	if type == 'public':
#		reply(type, source, u'Отправила в приват')
        if user_level(source[0], source[1]) == 100:
                 reply(type, source, u'Полный спикок команд'+pfx+superadmins+boss+chiefs+friend+owners+owner+admins+admin+moders+moder+users+user+level)
        if user_level(source[0], source[1]) == 80:
                 reply(type, source, u'Полный спикок команд'+pfx+chiefs+friend+owners+owner+admins+admin+moders+moder+users+user+level)
        if user_level(source[0], source[1]) == 30:
                 reply(type, source, u'Полный спикок команд'+pfx+owners+owner+admins+admin+moders+moder+users+user+level)
        if user_level(source[0], source[1]) == 20:
                 reply(type, source, u'Полный спикок команд'+pfx+admins+admin+moders+moder+users+user+level)
        if user_level(source[0], source[1]) == 15:
                 reply(type, source, u'Полный спикок команд'+pfx+moders+moder+users+user+level)
        if user_level(source[0], source[1]) == 10:
                 reply(type, source, u'Полный список команд'+pfx+users+user+level)


register_command_handler(command_comlist2, 'комлист', [], 10, 'Выводит список команд.', 'комлист', ['комлист'])

