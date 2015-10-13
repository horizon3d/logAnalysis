#! /usr/bin/python

class detr(object):

   def __init__(self, log):
      self.data = {}
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
      # get tid
      tid_pattern = r'detr tn[\s]*/([\d])'
      obj = re.match(tid_pattern, log, re.I)
      self.data['tid'] = obj.group(1)

      # get passenger
      passenger_pattern = r'PASSENGER: ([A-Za-z]+/[a-zA-Z]+)'
      obj = re.match(passenger_pattern, log, re.I)
      self.data['passenger'] = obj.group(1)

      # get ticket index
      self.data['ticket'] = []
      ticket_pattern = r':(\d{1})[\w]{3} ([A-Za-z]+)[\s]*([\d]+)([a-zA-Z]) (\d{2}[\w]{3}\d{4}) OK ([\w\s]+) RL:([A-Za-z0-9]+)'
      obj = re.match(ticket_pattern, log, re.I)
      while obj not None:
         ticket = {}
         ticket['company'] = obj.group(2)
         ticket['No'] = obj.group(3)
         ticket['magic'] = obj.group(4)

         month = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
         pattern = re.compile(r'(\d{2})([A-Z]{3}) (\d{4})')
         match = pattern.search(obj.group(5))
         mon = month[match.group(2)]
         day = match.group(1)
         time = match.group(3)
         year = strftime('%Y', gmtime())
         ts = mktime(strptime(year+ ' ' + mon + ' ' + day + time[0:2] + ':' + time[2:4] + ':' + ':00', '%Y %m %d %H:%M:%S'))

         ticket['time'] = ts
         ticket['state'] = obj.group(6)
         ticket['PNR'] = obj.group(7)
         self.data['ticket'].append(ticket)
         obj = re.match(ticket_pattern, log, re.I)