#===istalismanplugin===
# -*- coding: utf-8 -*-

from threading import Timer

class AutosendPlugin:
    def __init__(self):
      self.autosends = {}
    
    def install(self):
      def _handler(*args):
        self.message_handler(*args)
      
      register_command_handler(_handler, '!autosend', ['muc','all'], 100, 
                               'repeatly send a message with specified interval',
                               '!autosend <interval in seconds> <message>',
                               ['!autosend 30 jó napot kívánok', '!autosend off'])
    def add(self, groupchat, interval, message):
      def _autosend():
        try:
          (t, i, m) = self.autosends[groupchat]
          msg(groupchat, m)
          newtimer = Timer(i, _autosend)
          self.autosends[groupchat] = (newtimer, i, m)
          newtimer.start()
        except AttributeError:
          pass
      timer = Timer(interval, _autosend)
      self.autosends[groupchat] = (timer, interval, message)
      timer.start()
    def get(self, groupchat):
      return self.autosends[groupchat]
    def remove(self, groupchat):
      (timer, interval, message) = self.autosends.pop(groupchat)
      timer.cancel()
    
    def message_handler(self, type, source, parameters):
      global GROUPCHATS
      groupchat=source[1]
      if not groupchat in GROUPCHATS:
        reply(type, source, u'This command only possible in the conference')
        return
      args = parameters.strip().split(' ', 1)
      print(args)
      if len(args) == 0 or not (args[0]):
        try:
          (timer, interval, message) = self.get(groupchat)
          reply(type, source, u'autosending "%s" every %d seconds' % (message, interval))
        except KeyError:
          reply(type, source, u'no autosending here') 
        return
      elif len(args) == 1 and args[0] == "off":
        try:
          self.remove(groupchat)
          reply(type, source, u'autosending disabled')
        except KeyError:
          reply(type, source, u'autosending not enabled')
        return
      try:
        try:
          self.remove(groupchat)
        except KeyError:
          pass
        self.add(groupchat, int(args[0]), args[1])
        return
      except ValueError:
        pass
      reply(type, source, u'invalid syntax')

AutosendPlugin().install()
