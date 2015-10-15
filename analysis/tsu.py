#! /usr/bin/python

import re
from analysis.event import event
from analysis.error import (analyError, dbError)

class tsu(event):

   def __init__(self, adapter, log):
      super(event, self).__init__()
      self.convert(log)

      self.__dbAdapter = adapter
      self.__time = self.data['cmdTime']
      self.__cmd_pattern = re.compile(r'>tsu (\d{1})([/\S]*/open)', re.I)

   def __del__(self):
      pass

   def __check_forbbiden(self):

      cmd_pattern = re.compile(r'>tsu (\d{1})([/\S]*/open)', re.I)
      obj = cmd_pattern.search(self.data['message'])
      if obj:
         self.__ticket_idx = obj.group(1)
         self.__ticket_addition = obj.group(2)

      if re.match(r'/([OFECVR]|NM)', self.__ticket_addition, re.I):
         raise analyError('hit forbbiden element', self.data)

   def __check_detr(self, stage):

      parameter = stage['parameter']
      cmdName = stage['cmdName']

      #funcDict = {'strMatch':get_str, 'dateCmp':get_date}
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'],
                                           'cmd':{'$regex':'detr', '$options':'I'}, # cmdName --> 'detr'
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      
      if cr not None:
         detr = cr.next()
         tickets = detr['ticket']
         ticket = tickets[self.__ticket_idx - 1];
         state = ticket['state']
         if state.find('USED'):
            raise analyError('ticket has been already used', detr)
         elif state.find('OPEN FOR USED'):
            # OK, ticket is legal
            self.__detr = detr
      else:
         raise analyError('DETR option was not executed before tsu option', detr)

      if self.__detr['time'] < self.__time:
         raise analyError('ticket is over time', detr)

   def __check_rt(slef):
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'], 'pnr':self.__detr_pnr
                                           'cmd':{'$regex':'rt', '$options':'I'},
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      if cr not None:
         rt = cr.next()
         legal_pattern = re.compile('NO PNR'|'THIS PNR WAS ENTIRELY CANCELLED')
         obj = legal_pattern.search(rt['message'])
         if obj:
            return {'ok':1}

         ssrs = rt['ssr']
         for ssr in ssrs:
            if self.__detr['tn'] == ssr['tn'] and
               self.__detr['comp'] == ssr['comp'] and self.__detr['plane'] == ssr['plane'] and
               self.__detr['magic'] == ssr['magic'] and self.__detr['date'] == ssr['date'] and
               self.__detr['idx'] == ssr['idx'] :
               raise analyError('ticket is still valid', rt)
      else:
         raise analyError('cannot find rt log before tsu', self.data)

   def go(self, rule):
      self.__rule = rule
      stage = self.__rule['stage'][stageName]
      res = {}

      try:
         self.__check_forbbiden()
         self.__check_detr(stage)
         self.__check_date()
         self.__check_rt()
      except e:
         res = e.detail()

      return res