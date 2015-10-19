#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from helper import *

class spliter(object):
   def __init__(self):
      pass

   def __del__(self):
      pass

   def __convert(self, text):
      return text.encode('UTF-8')

   def get_user_sid(self, text):
      pattern = re.compile(r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: ([0-9]+)[-]+', re.I)
      match = pattern.match(text)
      usr = match.group(1)
      sid = match.group(2)

      return usr, sid

   def match(self, line):
      pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)', re.I)
      match = pattern.match(line)
      if match:
         return True
      return False

   def split(self, filename):
      fd = open(filename, 'r')
      user = ''
      sid = 0
      logs = []
      lines = []
      try:
         text = self.__convert(fd.readline())
         user, sid = self.get_user_sid(text)

         tmp = fd.readlines()
         for one in tmp:
            lines.append(self.__convert(one))
      except Exception, e:
         debug('Failed to read file: %s', filename)
      finally:
         fd.close()

         log = ''
         first = True
         for line in lines:
            if self.match(line):
               if first:
                  first = False
               else:
                  logs.append(log)
                  log = ''
            log += line

         if log != '':
            logs.append(log)

      return user, sid, logs

