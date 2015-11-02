#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.abspath('.') + os.sep + '..'))

import codecs
import time
import re
import linecache
from util.util import (LogError, LogEvent)

class tailfile(object):
   def __init__(self, filename):
      self.__filename = filename
      self.__rline = 0           # line number read
      self.__user = ''           # user
      self.__sid = 0             # sid
      self.__oneLog = ''         # the last log read
      self.__cache_log = []
      self.__cache_idx = 0
      self.__total = 0 # file line count
      self.__reg_usr_sid = r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: ([0-9]+)[-]+'
      self.__reg_ts      = r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)'

      self.__parse_cache()

   def __del__(self):
      linecache.clearcache()
      self.__rline = 0;

   @property
   def filename(self):
      return self.__filename

   @property
   def rline(self):
      return self.__rline

   @property
   def user(self):
      return self.__user

   @property
   def sid(self):
      return self.__sid

   def __convert(self, text):
      return text.encode('UTF-8')

   def __cached(self):
      total = 0
      fd = codecs.open(self.__filename, 'r', 'gbk')
      try:
         lines = fd.readlines()
         total = len(lines)
      except Exception, e:
         LogError('Failed to count file line: %s', self.__filename)
      finally:
         fd.close()

      return total, lines

   def __parse_cache(self):
      self.__total, lines = self.__cached()
      usr_sid_gotten = False
      first = True
      log = ''
      for line in lines:
         utext = self.__convert(line)
         if not usr_sid_gotten:
            if self.__match_usr_sid(utext):
               self.__user, self.__sid = self.__get_user_sid(utext)
               usr_sid_gotten = True
            else:
               continue
         else:
            if self.__match_date(utext):
               if first:
                  first = False
               else:
                  self.__cache_log.append(log)
                  log = ''
            log += utext

      if log != '':
         self.__oneLog = log
      self.__rline = self.__total

   def __get_user_sid(self, text):
      pattern = re.compile(r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: ([0-9]+)[-]+', re.I)
      match = pattern.match(text)
      usr = match.group(1)
      sid = match.group(2)

      return usr, sid

   def __match_date(self, line):
      pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)', re.I)
      match = pattern.match(line)
      if match:
         return True
      return False

   def __match_usr_sid(self, line):
      pattern = re.compile(r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: ([0-9]+)[-]+', re.I)
      match = pattern.match(line)
      if match:
         return True
      return False

   def __inc_line(self, line = 1):
      self.__rline += line

   def __is_line_valid(self):
      pass

   def __read_cache(self):
      log = None
      count = len(self.__cache_log)

      if self.__cache_idx < count:
         log = self.__cache_log[self.__cache_idx]
         self.__cache_idx += 1
         if self.__cache_idx == count:
            self.__cache_log = []
            self.__cache_idx = 0

      return log

   def next_log(self):

      if len(self.__cache_log) > 0:
         log = self.__read_cache()
         return log

      retry = True
      log = None
      while True:
         total, lines = self.__cached()
         if self.__rline < total:
            for line in lines[self.__rline:]:
               text = self.__convert(line)
               self.__inc_line()
               if text:
                  if self.__match_date(text):
                     if self.__oneLog:
                        log = self.__oneLog
                        self.__oneLog = text
                        break
                     else:
                        self.__oneLog = text
                  else:
                     self.__oneLog += text
         else:
            if retry:
               retry = False
               time.sleep(2)
            else:
               log = self.__oneLog
               self.__oneLog = ''
               break

      return log