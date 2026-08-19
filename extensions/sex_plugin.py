#===istalismanplugin===
# -*- coding: utf-8 -*-


sex_nicks={}

def handler_sex(type, source, parameters):
        if type=='private':
                reply(type,source,u';D')
                return
        groupchat = source[1]
        if parameters:
                if parameters==u'last10':
                        cnt=0
                        rep=''
                        nicks = set()
                        for x in [sex_nicks[source[1]] for x in sex_nicks]:
                                nicks = nicks | set(x)
                        for x in nicks:
                                cnt=cnt+1
                                rep += str(cnt)+u') '+x+u'\n'
                        reply('private',source,rep[:-1])
                        return
                if not source[1] in sex_nicks:
                        sex_nicks[source[1]]=source[1]
                        sex_nicks[source[1]]=[]
                if len(sex_nicks[source[1]])==10:
                        sex_nicks[source[1]]=[]
                else:
                        sex_nicks[source[1]].append(source[2])
                if not parameters == handler_botnick(source[1]):
                        if parameters in GROUPCHATS[source[1]]:
                                sexs=[]
                                sexs.extend(poke_work(source[1]))
                                sexs.extend(eval(read_file('static/sexs.txt'))['sex'])
                                rep = random.choice(sexs)
                                msg(source[1],(u'/me '+rep) % (parameters))
                        else:
                                reply(type, source, u'разве его жопа тут? :-O')
                else:
                        reply(type, source, u'я что дура по твоему,самa себя ипать? ]:->')	
        else:
                reply(type, source, u'отстань извращенец :D')
                
def poke_work(gch,action=None,phrase=None):
        DBPATH='dynamic/'+gch+'/sexs.txt'
        if check_file(gch,'sexs.txt'):
                pokedb = eval(read_file(DBPATH))
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
                
def remix_string(parameters):
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
        
register_command_handler(handler_sex, 'секс', ['все'], 10, 'ипёт юзера. Заставляет его обратить внимание на вас/на чат.\nlast10 вместо ника покажет список ников, которые ипались последними.', 'секс', ['секс qwerty'])