# BS mark.1
# coding: utf-8

#  BlackSmith plugin
#  Interpreter Plugin
#  Idea (c) Unknown Author
#  Code (c) simpleApps, 2011

def pyEval(mType, source, code):
   jid = handler_jid(source[0])
   if jid in [u'saranskcity@jabber.ru']:
      try: result = unicode(eval(code))
      except Exception: result = returnExc()
      reply(mType, source, result)
   else:
      reply(mType,source,u'Есть, отправляю жид!')
      delivery(u'Попытка использования команды eval юзером: '+jid)

def pyExec(mType, source, code):
   jid = handler_jid(source[0])
   if jid in [u'saranskcity@jabber.ru']:
      result = u"Done."
      try: exec(unicode(code + "\n"), globals())
      except Exception: result = returnExc()
      reply(mType, source, result)
   else:
      reply(mType,source,u'Есть, отправляю жид!')
      delivery(u'Попытка использования команды exec юзером: '+jid)

## PyShell is a name of one our project...
def pyShell(mType, source, cmd):
   jid = handler_jid(source[0])
   if jid in [u'saranskcity@jabber.ru']:
      if os.name == "posix":
         cmd = "sh -c \"%s\" 2>&1" % (cmd.encode("utf-8"))
      shell = os.popen(cmd)
      result = shell.read()
      if not result: result = "Done."
      reply(mType, source, result)
   else:
      reply(mType,source,u'Есть, отправляю жид!')
      delivery(u'Попытка использования команды sh юзером: '+jid)

def pyCalc(mType, source, expression):
        if expression and len(expression) <= 24 and not expression.count("**"):
                reg = re.sub(r"([0-9]|[\+\-\(\/\*\)\%\^\.])", "", expression)
                if reg:
                        result = "Недопустимо."
                else:
                        try:
                                result = eval(expression)
                        except ZeroDivisionError:
                                result = unichr(8734)
                        except Exception:
                                result = "An exception found."
        else:
                result = repr(None)
        reply(mType, source, str(result))

command_handler(pyEval, 10, "interpreter")
command_handler(pyExec, 10, "interpreter")
command_handler(pyShell, 10, "interpreter")
command_handler(pyCalc, 10, "interpreter")
