#! /usr/bin/python

import re
import copy
from task import baseTask
from error import (analyError, dbError)

funcMap = { 'CheckValid':'checkValid',
            'CheckDETRExist':'checkDETRExist',
            'CheckTicketState':'checkTicketState',
            'CheckTicketDate':'checkTicketDate'
          }
def checkValid(task, result):
   try:
      res = task.check_forbbiden()
   except e:
      result['errmsg'] = 'hit forbbiden element'
      result['msg'] = task.get()['message']
      raise

   if res not None:
      # 


def checkDETRExist(task, result):
   try:
      task.check_detr_exist()
   except analyError, e:
      raise

   if res not None:
      # 

def checkTicketState(task, result):
   try:
      task.check_detr_state()
   except analyError, e:
      raise

   if res not None:
      # 

def checkTicketDate(task, result):
   try:
      task.check_detr_date()
   except analyError, e:
      raise

   if res not None:
      # 

def checkRTExist(task, result):
   try:
      task.check_rt_exit()
   except analyError, e:
      raise

   if res not None:
      # 

def checkRTMatch(task, result):
   try:
      task.check_rt_match()
   except analyError, e:
      raise

class tsu(baseTask):

   def __init__(self, adapter, log):
      super(baseTask, self).__init__()
      self.convert(log)

      self.__dbAdapter = adapter
      self.__time = self.data['cmdTime']
      self.__store = {}

   def __del__(self):
      pass

   def append(self, key, value):
      if self.__store[key] not None:
         __debug('key[%s] exist, value: %s, it will be replaced by new value: %s', key, self.__store[key], value)

      self.__store[key] = value

   def check_forbbiden(self):
      cmd_pattern = re.compile(r'>[\s]*tsu (\d{1})([/\S]*/open)', re.I)
      obj = cmd_pattern.search(self.data['message'])
      if obj:
         self.append('tidx', int(obj.group(1)))
         self.__ticket_addition = obj.group(2)

      if re.match(r'/([OFECVR]|NM)', self.__ticket_addition, re.I):
         raise analyError('hit forbbiden element', self.data)

   """def __check_detr(self):

      #funcDict = {'strMatch':get_str, 'dateCmp':get_date}
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'],
                                           'cmd':{'$regex':'detr', '$options':'I'}, # cmdName --> 'detr'
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      
      if cr not None:
         detr = cr.next()
         tickets = detr['ticket']
         ticket = tickets[self.__store['tid'] - 1];
         state = ticket['state']
         if state.find('USED'):
            raise analyError('ticket has been already used', detr)
         elif state.find('OPEN FOR USED'):
            # OK, ticket is legal
            self.append('detr', detr)
      else:
         raise analyError('DETR option was not executed before tsu option', detr)

      if self.__detr['time'] < self.__time:
         raise analyError('ticket is over time', detr)
   """

   def check_detr_exist(self):
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'],
                                           'cmd':{'$regex':'detr', '$options':'I'}, # cmdName --> 'detr'
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      
      if cr not None:
         detr = cr.next()
         self.append('detr', detr)
      else:
         raise analyError('detr option is not done before!')

   def check_detr_state(self):

      detr = self.__store['detr']
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = tickets[self.__store['tid'] - 1];
         state = ticket['state']
         if state.find('USED'):
            raise analyError('ticket is used!')

   def check_detr_date(self):
      if self.__store['detr']['time'] < self.data['cmdTime']:
         raise analyError('ticket is expired!')

   def __check_rt(self):
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

   def check_rt_exist(self):
      detr = self.__store['detr']
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = tickets[self.__store['tid'] - 1];

      cr = self.__dbAdapter.query('log', { 'user':self.data['user'], 'pnr': ticket['pnr']
                                           'cmd':{'$regex':'rt', '$options':'I'},
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      
      if cr not None:
         rt = cr.next()
         self.append('rt', rt)
      else:
         raise analyError('rt option is not done before!')

   def check_rt_match(self):
      detr = self.__store['detr']
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = tickets[self.__store['tid'] - 1];

         ssrs = self.__store['']

   def go(self):
      self.__map()

"""
tsuRule = {
   
   'ruleType':'CMDFLOW',
   'tragger':{
      'cmdReturn':'ACCEPTED',
      'cmd':'TSU',
      'traggerType':'cmd'
   }
   'ruleGroup':'1',
   'ruleName':'TSU test',
   'stage':{
      '1':{
         'function':[ {'entry':'CheckValid', 'return':{'illegal':'ticket contais forbbiden flag!'}}},
                      {'entry':'CheckDETRExist', 'return':{'illegal':'detr option is not exist!'}},
                      {'entry':'CheckTicketState', 'return':{'illegal':'ticket is used!'}},
                      {'entry':'CheckTicketDate', 'return':{'illegal':'ticket is expired!'}} ],
         'return':{'legal':'2'},
         'cmdName':'DETR'
      }
      '2':{
         'function':[ {'entry':'CheckRTExist', 'return':{'illegal':'rt option is not exist!'}},
                      {'entry':'CheckRTMatch', 'return':{'illegal':'match a ticket that not used'}}} ],
         'return':{'legal':'final'}
         'cmdName':'RT'
      }
   }
}
"""
      

      result = {}
      for stageName in self.__stage_dict:
         stage = self.__rule['stage'][stageName]
         __debug('>>> current stage: %s', stageName)

         steps = stage['function']
         try:
         for step in steps:
            res = eval(funcMap[step['entry']][0])(self, result)
            if res == 'illegal':
               # result contains all info of error
               break
         except analyError,e:
            __debug('catch an exception: %s', r.detail)
            break

      endAnalysis(result)
      __debug('final result: %s', res)