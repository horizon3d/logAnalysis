#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import time
import re
from util.util import get_command
from util.util import (console, LogError, LogEvent)

month = { 'January':'01', 'February':'02', 'March':'03', 'April':'04', 
          'May':'05', 'June':'06', 'July':'07', 'August':'08',
          'September':'09', 'October':'10', 'November':'11', 'December':'12' }

shortMon = { 'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04',
             'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08',
             'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12' }

class event(object):
   def __init__(self, cmdName):
      self.__ctx = {}
      self.__ctx['cmd'] = cmdName

   def __del__(self):
      pass

   def data(self):
      return self.__ctx

   def __append_time(self, log):
      cmd_time = None
      pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)', re.I)
      match = pattern.search(log)
      if match:
         otime = match.group().split(',')
         ymd = otime[0]
         for (k, v) in month.items():
            ymd = ymd.replace(k,v)
         cmd_time = time.mktime(time.strptime((ymd + otime[2]), '%Y %m %d %H:%M:%S'))

      self.append('cmdTime', cmd_time)

   def __append_return(self, log):
      rtn = ''
      pattern = re.compile(r'>[\w /,:]+[\w][\s]*\n(.*)', re.I)
      match = pattern.search(log)
      if match:
         rtn = match.group(1)

      self.append('cmdReturn', rtn)

   def __append_input(self, log):
      cmd = ''
      pattern = re.compile(r'>([\w /,:]+[\w])[\s]*\n([\w /,:]+[\w])', re.I)
      match = pattern.search(log)
      if match:
         cmd1 = match.group(1)
         cmd2 = match.group(2)
         self.cmdInput = cmd1

         cmp1 = re.split('[:/, ]', cmd1)[0].upper()
         cmp2 = re.split('[:/, ]', cmd2[1:])[0].upper()

         if cmp1 == cmp2:
            cmd = cmd2[1:]
         else:
            cmd = cmd1.upper()

      if cmd == '':
         cmd = self.__ctx.get('cmd')

      self.append('cmdInput', cmd)

   def __append_flag(self, log):
      flag = True
      pattern = re.compile(r'\+[\s]*&', re.I)
      match = pattern.search(log)
      if match:
         flag = False
      self.append('flag', flag)

   def __append_cmd(self, log):
      if self.__ctx.get('cmd'):
         return

      pattern = re.compile(r'>[\s]*([\$\w]+) ')
      match = pattern.search(log)
      if match:
         self.append('cmd', match.group(1).upper())

   def append(self, k, v):
      if self.__ctx.get(k) is not None:
         console('key[%s] exist, value: %s, it will be replaced by new value: %s', k, self.__ctx[k], v)

      self.__ctx[k] = v

   def parse(self, log):
      self.__append_time(log)
      self.__append_input(log)
      self.__append_return(log)
      self.__append_flag(log)
      self.append('message', log)

   def get_match(self, pattern, log):
      return pattern.search(log)

   def to_json(self, log):
      self.parse(log)

class tsu(event):
   def __init__(self):
      event.__init__(self, 'TSU')

   def __del__(self):
      pass

   def __append_ticket_index(self, log):
      pattern = re.compile(r'>[\s]*tsu[\s:/]+((\w{1})[.*/:\w]+)', re.I)
      match = pattern.findall(log)
      if match:
         tid = match[0][1]
         self.append('index', tid)
         state = match[0][0]
         self.append('state', state)

   def __deep_parse(self, log):
      self.__append_ticket_index(log)


   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)

class detr(event):
   def __init__(self):
      event.__init__(self, 'DETR')

   def __del__(self):
      pass

   def __append_tn(self, log):
      pattern = re.compile(r'>[\s]*detr[\s:/]+tn[\s/:]*([\d]+)', re.I)
      match = pattern.search(log)
      if match:
         self.append('tn', match.group(1))
      else:
         LogError('no valid tn in detr context')
         LogError('log: \n%s', log)

   def __append_ticket(self, log):
      tickets = []
      pattern = r':(\d{1})\w+ ([\w]+)[ ]+([\d]+)[ ]+([a-zA-Z]) (\d{2}[\w]{3} \d{4}) OK ([\s\w/-]+)RL:([\w ]+)'
      match = re.findall(pattern, log, re.I)
      if not len(match):
         LogError('Warning: no valid ticket in detr context')
         LogError('log: \n%s', log)
      else:
         for obj in match:
            ticket = {}
            ticket['idx'] = int(obj[0])
            ticket['comp'] = obj[1]
            ticket['plane'] = obj[2]
            ticket['magic'] = obj[3]

            pattern = re.compile(r'(\d{2})([A-Z]{3}) (\d{4})')
            match = pattern.search(obj[4])
            mon = shortMon[match.group(2)]
            day = match.group(1)
            dtime = match.group(3)
            year = time.strftime('%Y', time.gmtime())
            ts = time.mktime(time.strptime(year+ ' ' + mon + ' ' + day + ' ' + dtime[0:2] + ':' + dtime[2:4] + ':00', '%Y %m %d %H:%M:%S'))

            ticket['time'] = ts
            ticket['state'] = obj[5]
            ticket['pnr'] = ''
            pnr = obj[6].strip()
            if pnr != '':
               ticket['pnr'] = pnr
            ticket['date'] = '' + match.group(1) + match.group(2)
            LogEvent('ticket: %s', str(ticket))
            tickets.append(ticket)
      self.append('ticket', tickets)

   def __deep_parse(self, log):
      self.__append_tn(log)
      self.__append_ticket(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)


class rt(event):
   def __init__(self):
      event.__init__(self, 'RT')

   def __del__(self):
      pass

   def __append_tkne(self, log):
      pattern = re.compile(r'>[\s]*rt[\s:/]+([\w]+)', re.I)
      match = pattern.search(log)
      if match:
         self.append('pnr', match.group(1))

      pattern = re.compile(r'SSR TKNE ([\w]+) [\w\d]+ [\w\d]+ (\d+) ([A-Z])(\d{2}\w{3}) (\d+)/(\d)/', re.I)
      obj = pattern.findall(log)

      tknes = []
      for item in obj:
         tkne = {}
         tkne['comp']  = item[0]
         tkne['plane'] = item[1]
         tkne['magic'] = item[2]
         tkne['date']  = item[3]
         tkne['tn']    = item[4]
         tkne['idx']   = item[5]
         LogEvent('SSR TKNE: %s', str(tkne))
         tknes.append(tkne)

      self.append('ssrtkne', tknes)

   def __deep_parse(self, log):
      self.__append_tkne(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)

class uu(event):
   def __init__(self):
      event.__init__(self, 'UU')

   def __del__(self):
      pass

   def __append_pid(self, log):
      pattern = re.compile(r'>[\s]*\w+[\s:/]+[a-zA-Z ]+ (\d+) [\w /]+')
      match = pattern.search(log)
      if match:
         self.append('pid', match.group(1))

   def __deep_parse(self, log):
      self.__append_pid(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)

class mo(event):
   def __init__(self):
      event.__init__(self, 'MO')

   def __del__(self):
      pass

   def __append_pid(self, log):
      pattern = re.compile(r'>[\s]*\w+[\s:/]+(\d+)\w+')
      match = pattern.search(log)
      if match:
         self.append('pid', match.group(1))

   def __deep_parse(self, log):
      self.__append_pid(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)

def usend(event):
   def __init__(self):
      event.__init__(self, 'SEND')

   def __del__(self):
      pass

   def __append_pid(self, log):
      pattern = re.compile(r'>[\s]*\w+[\s:/]+(\d+)\s\w+')
      match = pattern.search(log)
      if match:
         self.append('pid', match.group(1))

   def __deep_parse(self, log):
      self.__append_pid(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)

def text_to_json(log):
   cmd = get_command(log)
   if cmd is None:
      return None

   e = None
   if cmd == 'TSU':
      e = tsu()
   elif cmd == 'DETR':
      e = detr()
   elif cmd == 'RT':
      e = rt()
   #elif cmd == 'SEND':
      #e = usend()
   #elif cmd == 'MO':
      #e = mo()
   #elif cmd == 'UU':
      #e = uu()
   else:
      e = event(cmd)

   if e is not None:
      e.to_json(log)
   return e

