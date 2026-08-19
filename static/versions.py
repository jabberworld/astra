# caps\bot ver\core mod\bot rev\caps ver

Caps = 'http://miranda-im.org/caps'
BOT_VER = 3
CORE_MODE = 3
BOT_REV = 38
NONAME = 'Astra'
if os.access('.svn/entries', os.R_OK):
 try:
  BOT_REV = int(file('.svn/entries').readlines()[3].strip())
 except: 
  pass
  
CapsVer = '%d.%d' % (BOT_VER, CORE_MODE)
