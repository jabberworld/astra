#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin

#  Initial Copyright © 2007 Als <Als@exploru.net> 
#  remade: EugeNe

striptiz_nicks={}

def handler_striptiz(type, source, parameters):
        if type=='private':
                reply(type,source,u';D')
                return
        groupchat = source[1]
        if parameters:
                if parameters==u'last10':
                        cnt=0
                        rep=''
                        nicks = set()
                        for x in [striptiz_nicks[source[1]] for x in striptiz_nicks]:
                                nicks = nicks | set(x)
                        for x in nicks:
                                cnt=cnt+1
                                rep += str(cnt)+u') '+x+u'\n'
                        reply('private',source,rep[:-1])
                        return
                if not source[1] in striptiz_nicks:
                        striptiz_nicks[source[1]]=source[1]
                        striptiz_nicks[source[1]]=[]
                if len(striptiz_nicks[source[1]])==10:
                        striptiz_nicks[source[1]]=[]
                else:
                        striptiz_nicks[source[1]].append(source[2])
                if not parameters == handler_botnick(source[1]):
                        if parameters in GROUPCHATS[source[1]]:
                                striptize=[]
                                striptize.extend(poke_work(source[1]))
                                striptize.extend(load_file('static/striptize.txt', {})['striptizes'])
                                rep = random.choice(striptize)
                                if source[1] not in POL_SEX.keys():
                                          msg(source[1],u'/me '+rep % parameters)
                                else:
                                          reply(type, source, u'Только в нормальном режиме')
                        else:
                                reply(type, source, u'а он тут? :-O')
                else:
                        reply(type, source, u'я что дурa по твоему,самa себe? ]:->')	
        else:
                reply(type, source, u'отстань противный :D')
                
                
def poke_work5(gch,action=None,phrase=None):
        DBPATH='dynamic/'+gch+'/striptize.txt'
        if check_file(gch,'striptize.txt'):
                pokedb = load_file(DBPATH, {})
                if action==1:
                        for x in range(1, 21):
                                if str(x) in pokedb.keys():
                                        continue
                                else:
                                        pokedb[str(x)]=phrase
                                        write_file(DBPATH, str(pokedb))
                                        return True
                        return False
                elif action==2:
                        if phrase=='0':
                                pokedb.clear()
                                write_file(DBPATH, str(pokedb))
                                return True
                        else:
                                try:
                                        del pokedb[phrase]
                                        write_file(DBPATH, str(pokedb))
                                        return True
                                except:
                                        return False
                elif action==3:
                        return pokedb
                else:
                        return pokedb.values()
        else:
                return None
                
def remix_string5(parameters):
        remixed=[]
        for word in parameters.split():
                tmp=[]
                if len(word)<=1:
                        remixed.append(word)
                        continue
                elif len(word)==2:
                        tmp=list(word)
                        random.shuffle(tmp)
                        remixed.append(u''.join(tmp))
                elif len(word)==3:
                        tmp1=list(word[1:])
                        tmp2=list(word[:-1])
                        tmp=random.choice([tmp1,tmp2])
                        if tmp==tmp1:
                                random.shuffle(tmp)
                                remixed.append(word[0]+u''.join(tmp))
                        else:
                                random.shuffle(tmp)
                                remixed.append(u''.join(tmp)+word[-1])					
                elif len(word)>=4:
                        tmp=list(word[1:-1])
                        random.shuffle(tmp)
                        remixed.append(word[0]+u''.join(tmp)+word[-1])
        return u' '.join(remixed)
        
        
register_command_handler(handler_striptiz, 'стриптиз', ['все'], 10, 'стриптиз для юзера. Заставляет его обратить внимание на вас/на чат.\nlast10 вместо ника покажет список ников, которые смотрели стриптиз последними. Идея Евгениус', 'стриптиз <ник>|<параметр>', ['стриптиз qwerty','стриптиз + пришиб %s','стриптиз - 2','стриптиз *'])