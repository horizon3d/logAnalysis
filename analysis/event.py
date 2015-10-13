#! /usr/bin/python

from analysis.parser import parser
from analysis.util import *

__parser = None
__initialized = False

class event(object):

   def __init__(self):
      self.data = {}

   def __del__(self):
      pass

   def convert(self, log):

      if __parser is None:
         __parser = parser()
         __initialized = True

      __debug('log content: \r\n%s', log)
      parser.parse(log)

      self.data['user'] = __parser.user
      self.data['sid']  = __parser.sid
      self.data['cmdTime'] = __parser.time
      self.data['cmd']  = __parser.cmd
      self.data['cmdReturn'] = __parser.cmdReturn
      self.data['flag'] = __parser.flag
      self.data['message'] = log
      self.data['host'] = ''
      self.data['path'] = ''
      self.data['fileHeader'] = __parser.fileHeader

      __debug('event: %s', str(self.data))