#===istalismanplugin===
# -*- coding: utf-8 -*-

# by EugeNe



def handler_sexallb(type, source, parameters):
    try:
        if not source[1] in GROUPCHATS.keys():
            reply(type, source, u'only to chatrooms!')
            return
        SP = present_nicks(source[1])
        if len(SP) < 3:
            reply(type, source, u'мы тут в двоем походу!')
            return
        txt=read_file('static/kisses.txt')
        if not txt:
            reply(type, source, u'no joke in static/kisses.txt')
            return
        while SP:
            s=random.choice(SP)
            SP.remove(s)
            pokes=[]
            pokes.extend(load_file('static/kisses.txt', {})['kiss'])
            z=random.choice(pokes)
            if s!=handler_botnick(source[1]):
                msg(source[1], '/me '+z %s)
                time.sleep(1.5)
    except:
        raise
        reply(type, source, u'у когото из списка неприкосновенность,поэтому целовать не буду!')

register_command_handler(handler_sexallb, 'поцелуй_всех', ['все'], 10, 'Подобие тыка. Целует всех юзеров.', 'поцелуй_всех', ['поцелуй_всех'])