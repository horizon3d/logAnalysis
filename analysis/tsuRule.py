#! /usr/bin/python

import re

class tsu(object):

   def __init__(self, adapter, rule, ev):
      self.__dbAdapter = adapter
      self.__rule = rule
      self.__ev = ev
      self.__time = ev['cmdTime']
      self.__cmd_pattern = r'>tsu (\d{1})[/\S]*/open)'

   def __del__(self):
      pass

   def __check_forbbiden(self):
      res = None

      obj = re.match(self.__cmd_pattern, self.__ev['message'], re.I)
      if obj:
         self.__ticket_idx = obj.group(1)
         self.__ticket_addition = obj,.group(2)

      if re.match(r'([OFECVR]/|NM)', self.__ticket_addition, re.I):
         res = {'illegal':'hit forbbiden element'}

      return res

   def __check_detr(self, stage):

      parameter = stage['parameter']
      cmdName = stage['cmdName']

      funcDict = {'strMatch':get_str, 'dateCmp':get_date}
      cr = self.__dbAdapter.query('log', { 'user':self.__ev['user'],
                                           'cmd':{'$regex':cmdName, '$options':'I'},
                                           'cmdTime':{'$lt':ev['cmdTime']}
                                         })
      
      if cr not None:
         res = None

         detr = cr.next()
         tickets = detr['ticket']
         ticket = tickets[self.__ticket_idx - 1];
         state = ticket['state']
         if state.find('USED'):
            res = {'illegal':'ticket has been already used'}
         elif state.find('OPEN FOR USED'):
            # OK, ticket is legal
            self.__detr_comp = ticket['company']
            self.__detr_air  = ticket['No']
            self.__detr_airtime = ticket['time']
            self.__detr_pnr = ticket['pnr']
      else:
         res = {'illegal':'DETR option was not executed before tsu option'}

      return res

   def __check_date(self):
      res = None

      if self.__detr_airtime < self.__time:
         res = {'illegal':'ticket time is over'}

      return res

   def go(self):

      step = 1

      stage = self.__rule['stage'][stageName]
      res = 'Error'
      
      returnCond = stage['returnCondition']

      while True:
         if 1 == step:
            res = self.__check_forbbiden()
         elif 2 == step:
            res = self.__check_detr(stage)
         elif 3 == step:
            res = self.__check_date()
         elif 4 == step:
            res = self.__check_rt()
         elif 5 == step:

            
         if res not None:
               break
            else:
               step = step + 1

      return res