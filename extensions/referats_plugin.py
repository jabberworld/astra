#===istalismanplugin===
# -*- coding: utf-8 -*-
import urllib.request as urllib2

# автор - ferym@jabbim.org.ru
# по вопросам обращаться в support@conference.veganet.org.ru
# web site: http://veganet.org
# plugin version 1.0

def handler_refer(type, source, parameters):
    if not parameters:
      reply(type, source, u'выберите категорию реферата!\nподробнее "помощь реферат"')
      return
    elif parameters==u'астрономия':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/astronomy.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
      
    elif parameters==u'геология':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/geology.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
      
    elif parameters==u'гироскопия':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/gyroscope.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
      
    elif parameters==u'литература':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/literature.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'маркетинг':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/marketing.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'математика':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/mathematics.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'музыка':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/music.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'политология':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/polit.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'почвоведение':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/agrobiologia.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'правоведение':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/law.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'психология':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/psychology.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'география':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/geography.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'физика':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/physics.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'философия':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/philosophy.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'химия':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/chemistry.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
              
    elif parameters==u'эстетика':
      try:
          if parameters.strip() != '':
              reply(type, source, eval(parameters.strip()))
          else:
              r = urllib2.urlopen(req)
      except:
          req = urllib2.Request('http://referats.yandex.ru/estetica.xml')
          req.add_header = ('User-agent', 'Mozilla/5.0')
          r = urllib2.urlopen(req)
          target = r.read()
          od = re.search('<h1 style="color:black; margin-left:0;">',target)
          message = target[od.end():]
          message = message[:re.search('</div></td>',message).start()]
          message = '\n' + message.strip()
          message = decode(message)
          if type=='private':
            reply(type, source, unicode(message,'windows-1251'))
          else:
            reply(type, source, u'ушло в приват')
            reply('private', source, unicode(message,'windows-1251'))
            return
    
    elif parameters==u'категории':
      categ = [u'астрономия',u'геология',u'гироскопия',u'литература',u'маркетинг',u'математика',u'музыка',u'политология',u'почвоведение',u'правоведение',u'психология',u'география',u'физика',u'философия',u'химия',u'эстетика']
      repl = u'Доступны рефераты по следующим категориям:\n'+',\n'.join(categ)+u'\nВсего ('+str(len(categ))+u') категорий.\nЧто бы сгенерировать реферат по определённой категории, выполните команду "реферат <категория>\nby ferym"'
      reply(type, source, repl)
            
            
    else:
      reply(type, source, u'Не существующая категория!\nподробнее "помощь реферат"')
      return           
                  
def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n').replace('<\h1>','\n \n').replace('<p>','').replace('<\p>',''))

register_command_handler(handler_refer, 'реферат', ['mod','все'], 10,'Генерация рефератов по выбранным вами темам.\nДля просмотра доступных категорий выполните команду "реферат категории"','реферат <категория>', ['реферат философия','реферат категории\nby ferym\nplugin version 1.0'])