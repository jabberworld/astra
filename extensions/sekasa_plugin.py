#===istalismanplugin===
# -*- coding: utf-8 -*-

# by EugeNe



def handler_sexallaa(type, source, parameters):
    try:
        if not source[1] in GROUPCHATS.keys():
            reply(type, source, u'only to chatrooms!')
            return
        SP=[]
        for x in GROUPCHATS[source[1]]:
            if GROUPCHATS[source[1]][x]['ishere']:
                SP.append(x)
        if not len(SP)>2:
            reply(type, source, u'мы тут в двоем походу!')
            return
        txt=read_file('static/delirium.txt')
        if not txt:
            reply(type, source, u'no joke in static/sexs.txt')
            return
        while SP:
            s=random.choice(SP)
            SP.remove(s)
            pokes=[]
            pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
            z=random.choice(pokes)
            if s!=handler_botnick(source[1]):
                msg(source[1], '/me '+z %s)
                time.sleep(1.5)
    except:
        raise
        reply(type, source, u'у когото из списка неприкосновенность,поэтому тыкать не буду!')

register_command_handler(handler_sexallaa, 'тык_всех', ['все'], 10, 'Подобие тыка. Тык всех юзеров.', 'тык_всех', ['тык_всех'])