#===istalismanplugin===
# -*- coding: utf-8 -*-

import urllib.request as urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')
          
def decode_s(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

def hnd_fun_k(type,source,parameters):
        ALL=[]
        if type=='private':
                return
        NO=[u'дала па галаве веником',u'нехватило',u'не насыпала',u'плюнула в миску']
        if source[1] in GROUPCHATS:
                n=0
                for x in GROUPCHATS[source[1]]:
                        if GROUPCHATS[source[1]][x]['ishere']==1:
                                n+=1
                                ALL.append(x)
                if n<3:
                        reply(type,source,u'зови народ,тогда и зохаваем!')
                        return
                no=random.choice(ALL)
                yes=''
                for x in ALL:
                        if x!=no:
                                yes+=u'насыпала '+x+'\n'
                msg(source[1],yes)
                time.sleep(1.5)
                msg(source[1],u'a '+no+' '+random.choice(NO))

def hnd_lust_ru(type,source,parameters):
        #http://www.notproud.ru/lust/
        try:
                req = urllib2.Request('http://www.notproud.ru/random.html')
                req.add_header = ('User-agent', 'Mozilla/5.0')
                r = urllib2.urlopen(req)
                text = r.read()
                od = re.search('<td align="left" valign="top" class="font2">',text)
                rep = text[od.end():]
                rep = rep[:re.search('</tr>',rep).start()]
                rep=decode_s(rep)
                if rep=='':
                        return
                if rep.isspace():
                        reply(type,source,u'наверное разметку сменили')
                        return
                reply(type,source,unicode(rep,'utf-8'))
        except:
                reply(type,source,u'unknown error')
                               
register_command_handler(hnd_lust_ru, 'признание', ['фан','все'], 10, 'признание с http://www.notproud.ru/lust/', 'признание', ['признание'])                
register_command_handler(hnd_fun_k, 'каша', ['фан','все'], 10, 'раздача каши', 'каша', ['каша'])                               
