#===istalismanplugin===
# /* coding: utf-8 */

#  Talisman Bot plugin
#  bomba_plugin.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

COLOR = [u'красный', u'зеленый', u'синий', u'голубенький', u'белый', u'желтый', u'серый', u'оранжевый', u'фиолетовый', u'серо-буро-малиновый']

PROVOD = {}

def color_norm(s):
        return (s or u'').strip().lower().replace(u'ё', u'е')

def bomb_key_for(nick):
        t = color_norm(nick)
        for key in PROVOD:
                if color_norm(key) == t:
                        return key
        return None

def bomb(type, source, args):
        if source[1] in GROUPCHATS:
                if args:
                        nick = args.strip()
                        if user_level(source[0], source[1]) < 15 and nick != source[2]:
                                reply(type, source, u'ты можешь взрывать только себя')
                                return
                        if not nick in GROUPCHATS[source[1]] or not GROUPCHATS[source[1]][nick]['ishere']:
                                reply(type, source, u'юзера с таким ником здесь нет')
                                return
                else:
                        nick = source[2]
                if user_level(source[1]+'/'+nick, source[1]) < 15:
                        provoda = []
                        for prv in COLOR:
                                if len(provoda) < 2 or random.randrange(1, 10) >= 7:
                                        provoda.append(prv)
                        provod = random.choice(provoda)
                        PROVOD[nick] = color_norm(provod)
                        time = random.randrange(15, 45)
                        msg(source[1], nick+u': вам вручена бомба, на ней '+str(len(provoda))+u' провода(ов): '+', '.join(provoda)+u' выберите цвет провода который нужно перерезать, на таймере '+str(time)+u' секунд')
                        try:
                                threading.Timer(time, bomb_start,(source[1], nick)).start()
                        except:
                                pass
                else:
                        reply(type, source, u'модеры не взрываются!')
        else:
                reply(type, source, u'ты дурак?')

def bomb_start(conf, nick):
        key = bomb_key_for(nick)
        if key:
                here = GROUPCHATS.get(conf, {}).get(key, {}).get('ishere')
                if here:
                        msg(conf, nick+u': ПТЫДЫЩЬ! Время вышло, вы не успели перерезать провод!')
                        handler_kick(conf, key, u'время вышло! птыдыщь!')
                del PROVOD[key]

def bomb_msg(raw, type, source, body):
        key = bomb_key_for(source[2])
        if key:
                answer = color_norm(body)
                if answer == PROVOD[key]:
                        reply(type, source, u'бомба обезврежена!')
                        del PROVOD[key]
                else:
                        reply(type, source, u'птыдыщь! не тот провод, надо было перерезать: '+PROVOD[key])
                        handler_kick(source[1], key, u'птыдыщь!')
                        del PROVOD[key]

register_message_handler(bomb_msg)
command_handler(bomb, 10, "bomba")
