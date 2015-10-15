#! /usr/bin/python

import re
from analysis.event import event

__month = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}

class detr(event):

   def __init__(self, log):
      super(event, self).__init__()
      self.convert(log)

      self.data['cmd'] = 'detr'
      self.__flat(log)

   def __del__(self):
      pass

   def __flat(self, log):
      """
      2015 September 22, Tuesday, 16:54:57
>detr tn  9999686012042 
 DETR:TN  9999686012042                                                        
ISSUED BY: AIR CHINA                 ORG/DST: BJS/SHA                 BSP-I     
E/R: 9BJ10G0C/NONEND                                                            
TOUR CODE: X9BJ10G0C                                         RECEIPT PRINTED  
PASSENGER: DONG/XUEMIN                                                          
EXCH:                               CONJ TKT:                                   
O FM:1PEK CA     995  Z 08SEP 1500 OK ZXAP7H/NA  08SEP5/08SEP5 2PC USED/FLOWN   
     T3-- RL:NB416S  /HS3N8R1E BG:2/43K BN:149                                  
O TO:2IAH CA     996  Z 25SEP 0100 OK ZWAP7H/NA  25SEP5/25SEP5 2PC OPEN FOR USE 
     --T3 RL:NB416S  /HS3N8R1E                                                  
X TO:3PEK CA    1831  F 26SEP 0730 OK F/NA       26SEP5/26SEP5 2PC OPEN FOR USE 
     T3T2 RL:NB416S  /HS3N8R1E                                                 +
      """
      # get tn
      tn_pattern = re.compile(r'>detr tn[\s/]+([\d]+)', re.I)
      obj = tid_pattern.search(log)
      self.data['tn'] = obj.group(1)

      # get passenger
      passenger_pattern = re.compile(r'PASSENGER: ([A-Za-z]+/[a-zA-Z]+)', re.I)
      obj = passenger_pattern.search(log)
      self.data['passenger'] = obj.group(1)

      # get ticket index
      ticket_pattern = r':(\d{1})[\w]{3} ([A-Za-z]+)[\s]*([\d]+)[\s]+([a-zA-Z]) (\d{2}[\w]{3} \d{4}) OK ([\w/\s]+) RL:([\w ]+) [\w\s]*'
      tickets = re.findall(ticket_pattern, log, re.I)
      if len(tickets):
         self.data['ticket'] = []

      for obj in tickets:
         ticket = {}
         ticket['idx'] = obj[0]
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