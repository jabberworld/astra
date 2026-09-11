# caps\bot ver\core mod\bot rev\caps ver

Caps = 'http://miranda-im.org/caps'
BOT_VER = 4
CORE_MODE = 4
BOT_REV = 10
NONAME = 'Astra'
if os.access('.svn/entries', os.R_OK):
 try:
  BOT_REV = int(file('.svn/entries').readlines()[3].strip())
 except: 
  pass
  
CapsVer = '%d.%d' % (BOT_VER, CORE_MODE)
