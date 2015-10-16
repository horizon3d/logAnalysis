#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from task import baseTask

__month = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}

class detrTask(baseTask):

   def __init__(self, data):
      super(baseTask, self).__init__()
      self.convert(log)

      self.__flat(log)

   def __del__(self):
      pass

   def __flat(self, log):
      # get tn
      tn_pattern = re.compile(r'>detr tn[\s/]+([\d]+)', re.I)
      obj = tn_pattern.search(log)
      self.data['tn'] = obj.group(1)

      # get passenger
      passenger_pattern = re.compile(r'PASSENGER: ([A-Za-z]+/[a-zA-Z]+)', re.I)
      obj = passenger_pattern.search(log)
      self.data['passenger'] = obj.group(1)

      # get ticket index
      ticket_pattern = r':(\d{1})\w+ ([\w]+)[ ]+([\d]+)[ ]+([a-zA-Z]) (\d{2}[\w]{3} \d{4}) OK ([\s\w/-]+):(\w+)'
      tickets = re.findall(ticket_pattern, log, re.I)
      if len(tickets):
         self.data['ticket'] = []

      for obj in tickets:
         ticket = {}
         ticket['idx'] = int(obj[0])
         ticket['comp'] = obj[1]
         ticket['plane'] = obj[2]
         ticket['magic'] = obj[3]

         pattern = re.compile(r'(\d{2})([A-Z]{3}) (\d{4})')
         match = pattern.search(obj[4])
         mon = __month[match.group(2)]
         day = match.group(1)
         time = match.group(3)
         year = strftime('%Y', gmtime())
         ts = mktime(strptime(year+ ' ' + mon + ' ' + day + time[0:2] + ':' + time[2:4] + ':' + ':00', '%Y %m %d %H:%M:%S'))

         ticket['time'] = ts
         ticket['state'] = obj[5]
         ticket['pnr'] = obj[6]
         ticket['date'] = '' + match.group(1) + match.group(2)
         self.data['ticket'].append(ticket)