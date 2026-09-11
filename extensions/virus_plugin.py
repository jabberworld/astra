#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  commoff_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

        
def handler_test(type, source, parameters):
        mas = [u'пассед',
                        u'Пиши "хелп" :-O :-[ ой... блин... >пассед<',
                        u'Извини... не сегодня...',
                        u'Я тут посплю часок',
                        u'Я в поряде',
                        u'Аа-аа-а ссс-ууука-аа',
                        u'полный абзац...',
                        u'Я безотказен как автомат "Калашникова"',
                        u'Я не сплю',
                        u'Атстань пративный!',
                        u'Нууу... противный... не мешай спать zZzZ',
                        u'Ломай меня полностью! :-D',
                        u'Я хочу чтоб ты ломал меня :-[']
        rap = random.choice(mas)
        reply(type,source,rap)
        
virus = [u'Net-Worm.Win32.Mytob.bd', u'Worm.ExploreZip', u'Trojan.Generic', u'097/Crown.B', u'I-Worm.Mydoom.q', u'Trojan-Dropper.Win32.Microjoin.l', u'Worm.Win32.Feebs.gen_07', u'Win32.HLLM.Graz.00', u'VBS.Redlof.a', u'Joke.Flipped', u'Program.HiddenAdmin.origin', u'I-Worm.Tanatos.a', u'unknown', u'вирусов не нашел']
act = [u'[Лечение невозможно]', u'[Вылечен]']
antivirus = [u'Eset (NOD32)', u'avast 7.4', u'Norman', u'kaspersky 2009', u'Panda', u'Symantec']

def handler_test_virus(type, source, parameters):
        reply(type,source,u'начинаю сканировать комнату на вирусы...')
        time.sleep(random.randrange(0, 6))
        reply(type,source,u'...запускаю антивирус <'+random.choice(antivirus)+u'> Подождите...')
        time.sleep(random.randrange(0, 30))
        ocupants = []
        for i in GROUPCHATS[source[1]]:
                if GROUPCHATS[source[1]][i]['ishere'] == 1:
                        ocupants.append(i)
        if len(ocupants) > 10:
                count = random.randrange(0, 10)
        else:
                count = random.randrange(0, len(ocupants))
        if count == 0:
                res= u'Вирусов не обнаружено'
        else:
                res = u'Найдено '+str(count)+u' вирусов:'
                for vir in range(0, count):
                        res += '\n'+random.choice(ocupants)+' ('+random.choice(virus)+') '+random.choice(act)
        reply(type,source, res)


register_command_handler(handler_test_virus, 'скан', ['все'], 30, '...', '...', ['...']) 	

#register_command_handler(handler_test, 'тест', ['все'], 10, 'Тупо отвечает пассед.', 'тест', ['тест'])
#register_command_handler(handler_test, 'test', ['все'], 10, 'Тупо отвечает пассед.', 'test', ['test'])
