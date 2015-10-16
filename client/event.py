#! /usr/bin/python
# -*- coding:utf-8 -*-

import time
import re
from helper import *

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

   def get(self):
      return self.__ctx

   def __get_time(self, log):
      pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)', re.I)
      match = pattern.search(log)
      if match:
         otime = match.group().split(',')
         ymd = otime[0]
         for (k, v) in month.items():
            ymd = ymd.replace(k,v)
      return time.mktime(time.strptime((ymd + otime[2]), '%Y %m %d %H:%M:%S'))

   def __get_return(self, log):
      pattern = re.compile(r'[\w /,:]+[\w][\s]*\n(.*)', re.I)
      match = pattern.search(log)
      if match:
         rtn = match.group(1)
         __debug('return: %s', rtn)
      return rtn

   def __get_input(self, log):
      pattern = re.compile(r'>([\w /,:]+[\w])[\s]*\n([\w /,:]+[\w])', re.I)
      match = pattern.search(log)
      if match:
         cmd1 = match.group(1)
         cmd2 = match.group(2)
         self.cmdInput = cmd1

         cmp1 = re.split('[:/, ]', cmd1)[0].upper()
         cmp2 = re.split('[:/, ]', cmd2[0:])[0].upper()

         if cmp1 == cmp2:
            cmd = cmd2[1:]
         else:
            cmd = cmd1.upper()
      #__debug('input: %s', cmd)
      return cmd

   def __get_flag(self, log):
      flag = True
      pattern = re.compile(r'\+[\s]*&', re.I)
      match = pattern.search(log)
      if match:
         flag = False
      return flag

   def append(self, k, v):
      if self.__ctx.get(k) is not None:
         __debug('key[%s] exist, value: %s, it will be replaced by new value: %s', k, self.__ctx[k], v)

      self.__ctx[k] = v

   def parse(self, log):
      self.append('cmdTime', self.__get_time(log))
      self.append('cmdInput', self.__get_input(log))
      self.append('cmdReturn', self.__get_return(log))
      self.append('flag', self.__get_flag(log))
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
      pattern = re.compile(r'>[\s]*tsu ((\w{1})[.*/:\w]+)', re.I)
      match = pattern.findall(log)
      if match:
         tid = match[0][1]
         __debug('ticket id is: %s', tid)
         self.append('index', tid)
         state = match[0][0]
         __debug('state is: %s', state)
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
      pattern = re.compile(r'>[\s]*detr tn[\s/]+([\d]+)', re.I)
      match = pattern.search(log)
      if match:
         self.append('tn', match.group(1))
      else:
         __debug('find no match tn in detr context')
         return None

   def __append_passenger(self, log):
      pattern = re.compile(r'PASSENGER: ([A-Za-z]+/[a-zA-Z]+)', re.I)
      match = pattern.search(log)
      if match:
         self.append('passenger', match.group(1))
      else:
         __debug('find no match passenger in detr context')

   def __append_ticket(self, log):
      pattern = r':(\d{1})\w+ ([\w]+)[ ]+([\d]+)[ ]+([a-zA-Z]) (\d{2}[\w]{3} \d{4}) OK ([\s\w/-]+):(\w+)'
      match = re.findall(pattern, log, re.I)
      if len(match):
         tickets = []
         self.data['ticket'] = []
      else:
         __debug('find no match ticket in detr context')
         return None

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
         time = match.group(3)
         year = strftime('%Y', gmtime())
         ts = mktime(strptime(year+ ' ' + mon + ' ' + day + time[0:2] + ':' + time[2:4] + ':' + ':00', '%Y %m %d %H:%M:%S'))

         ticket['time'] = ts
         ticket['state'] = obj[5]
         ticket['pnr'] = obj[6]
         ticket['date'] = '' + match.group(1) + match.group(2)
         __debug('ticket: %s', str(tickets))
         tickets.append(ticket)

      self.append('ticket', tickets)

   def __deep_parse(self, log):
      self.__append_tn()
      self.__append_passenger()
      self.__append_ticket()

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)


class rt(event):
   def __init__(self):
      event.__init__(self, 'RT')

   def __del__(self):
      pass

   def __append_tkne(self, log):
      pattern = re.compile(r'>[\s]*rt ([\w]+)', re.I)
      match = pattern.search(log)
      if match:
         self.append('pnr', match.group(1))

      pattern = re.compile(r'SSR TKNE ([\w]+) [\w\d]+ [\w\d]+ (\d+) ([A-Z])(\d{2}\w{3}) (\d+)/(\d)/', re.I)
      obj = pattern.findall(log)

      tknes = []
      for item in obj:
         tnke = {}
         tnke['comp']  = item[0]
         tnke['plane'] = item[1]
         tnke['magic'] = item[2]
         tnke['date']  = item[3]
         tnke['tn']    = item[4]
         tnke['idx']   = item[5]
         tknes.append(tnke)

      self.append('ssrtkne', tknes)

   def __deep_parse(self, log):
      self.__append_tkne(log)

   def to_json(self, log):
      self.parse(log)
      self.__deep_parse(log)
