#! /usr/bin/python
# -*- coding:utf-8 -*-

class spilter(object):
   def __init__(self):
      pass

   def __del__(self):
      pass

   def get_user_sid(self, text):
      pattern = re.compile(r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: ([0-9]+)[-]+', re.I)
      match = pattern.match(text)
      usr = match.group(1)
      sid = match.group(2)

      return usr, sid

   def __match_date(self, line):
      match = False
      pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+) (>[\s\w=-:/]+)', re.I)
      obj = pattern.search(line)
      if obj :
         match = True

      return match

   def spilt(self, filename):
      try:
         fd = open(filename, 'r')
         text = fd.readline()

         user, sid = self.get_user_sid(text)

         lines = fd.readlines()
         logs = []
         log = ''
         for line in lines:
            if len(line) and match:
               logs.append(log)
               log = ''
            log = log + line
            
         if log != '':
            logs.append(log)

      finally:
         fd.close()

      return logs

