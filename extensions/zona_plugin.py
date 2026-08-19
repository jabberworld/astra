#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  zona_plugin.py

#  Author: Als [Als@exploit.in]
#  Modifications: metalist [metalist@jabbik.org]

def handler_zona(type, source, nick):
        if type == 'public':
                if nick:
                        if not nick == handler_botnick(source[1]):
                                if nick in GROUPCHATS[source[1]]:
                                        zonas = []
                                        zonas.extend(zona_work(source[1]))
                                        zonas.extend(load_file('static/zona.txt', {})['zona'])
                                        repl = random.choice(zonas)
                                        msg(source[1], u'/me '+repl % (nick))
                                else:
                                        reply(type, source, u'его ни хуя нету')
                        else:
                                reply(type, source, u'пшел в пизду!')
                else:
                        reply(type, source, u'мазохист и онанист? :D')
        else:
                reply(type, source, u'хуй')

def handler_zona_control(type, source, body):
        if body:
                args = body.split()
                if len(args) >= 2:
                        cmd = args[0].strip().lower()
                        if cmd in [u'адд', '+']:
                                text = body[(body.find(' ') + 1):].strip()
                                if text.count('%s'):
                                        if zona_work(source[1], 1, text):
                                                reply(type, source, u'чпок')
                                        else:
                                                reply(type, source, u'хуй!раскатал губу.')
                                else:
                                        reply(type, source, u'не вижу ни хуя %s')
                        elif cmd in [u'дел', '-']:
                                text = args[1].strip()
                                if check_number(text):
                                        if zona_work(source[1], 2, text):
                                                reply(type, source, u'пизда')
                                        else:
                                                reply(type, source, u'такой ни хуя нет')
                                else:
                                        reply(type, source, u'ты инвалид и твой синтакс')
                        else:
                                reply(type, source, u'ты инвалид и твой синтакс')
                else:
                        reply(type, source, u'ты инвалид и твой синтакс')
        else:
                repl, res = '', zona_work(source[1], 3)
                if res:
                        res = sorted(res.items(), lambda x,y: int(x[0]) - int(y[0]))
                        for num, phrase in res:
                                repl += num+') '+phrase+'\n'
                        reply(type, source, repl.strip())
                else:
                        reply(type, source, u'нет долбаебских выдумок')

def zona_work(conf, action = None, phrase = None):
        if check_file(conf, 'zona.txt'):
                base = 'dynamic/'+conf+'/zona.txt'
                try:
                        zonadb = load_file(base, {})
                except:
                        zonadb = {}
                if action == 1:
                        for number in range(1, 21):
                                if str(number) not in zonadb:
                                        zonadb[str(number)] = phrase
                                        write_file(base, str(zonadb))
                                        return True
                        return False
                elif action == 2:
                        if phrase == '0':
                                zonadb.clear()
                                write_file(base, str(zonadb))
                                return True
                        elif phrase in zonadb:
                                del zonadb[phrase]
                                write_file(base, str(zonadb))
                                return True
                        else:
                                return False
                elif action == 3:
                        return zonadb
                else:
                        zonas = []
                        for zona in zonadb.values():
                                zonas.append(zona)
                        return zonas
        return False

register_command_handler(handler_zona, 'опустить', ['фан','все'], 10, 'Опускает юзера, как на зоне\nRemade by metalist\nP.S. Я служу для jabbik team\nВот и хуй всем остальным!', 'опустить <ник>|<параметр>', ['опустить Вася'])
register_command_handler(handler_zona_control, 'опустить*', ['фан','все'], 20, 'добавить или удалить фразу.\n%s - переменная ника.\n/me - переменная выделения.\nБез параметров покажет список фраз\nRemade by metalist\nP.S. Я служу для jabbik team\nВот и хуй всем остальным!', 'опустить* [+/адд/-/дел]', ['опустить* + изнасиловал %s','опустить* - 4','опустить*'])
