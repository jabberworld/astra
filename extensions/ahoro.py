#===istalismanplugin===
# -*- encoding: utf-8 -*- #

# Coded by mrDoctorWho [JID: nexus@xmpp.ru]
# Only for Witcher Team [SITE: http://witcher-team.ucoz.ru]

from urllib.request import urlopen
from re import search

aHoroItems = {u"рак": "ca",
              u"лев": "le",
                          u"дева": "vi",
              u"весы": "li",
                          u"рыбы": "pi",
                          u"овен": "ar",
              u"телец": "ta",
              u"козерог": "cp",
              u"водолей": "aq",
                          u"стрелец": "sa",
              u"козлорог": "cp",
                          u"скорпион": "sc",
                          u"близнецы": "ge"} # with easter egg ;)

def replacer(what):
        return what.replace("&#0o151;", "-").replace("</h4><p>","")

def getHoro(mHoro):
        OpenSite = urlopen("http://brb.silverage.ru/anti/?sign=%s" % (mHoro))
        isText = OpenSite.read().decode("cp1251")
        od = search('<h4>', isText)
        TheEnd = isText[od.end():]
        aHoro = TheEnd[:search('<br><br></p>', TheEnd).start()]
        return replacer(aHoro)

def horo_answer(type, source, body):
   if body:
      if body in aHoroItems:
         repl = getHoro(aHoroItems[body])
      elif body == u"все":
         repl = u"Список знаков зодиака:\n" + ", ".join(aHoroItems)
      elif body not in [u"все",u"лев",u"дева",u"весы",u"рыбы",u"рак",u"овен",u"телец",u"козерог",u"водолей",u"стрелец",u"козлорог",u"скорпион",u"близнецы"]:
         repl = u"не гони! только знаки зодиака!"
   else:
      global A_HORO
      jid = handler_jid(source[0])
      if jid in A_HORO.keys():
         body = A_HORO[jid]
         if body in aHoroItems:
            repl = getHoro(aHoroItems[body])
         else:
            repl = u"Проверь данные анкеты!"
      else:
         repl = u"Я не экстрасенс :)"
   reply(type, source, repl)

register_command_handler(horo_answer, 'антигороскоп', ['инфо','все'], 10, 'Антигороскоп - не поймите его правильно!', 'антигороскоп <знак зодиака/все>', ['антигороскоп все', 'антигороскоп овен'])
