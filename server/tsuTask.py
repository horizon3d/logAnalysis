#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from task import baseTask
from error import (analyError, dbError)
from util import *

funcMap = {
            'CheckValid':'checkValid',
            'CheckDETRExist':'checkDETRExist',
            'CheckTicketState':'checkTicketState',
            'CheckTicketDate':'checkTicketDate',
            'CheckRTExist':'checkRTExist',
            'CheckRTMatch':'checkRTMatch'
          }

def checkValid(task, result):
   try:
      task.check_forbbiden()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = []
      result['cmdInput'] = task.get('cmdInput')
      raise

def checkDETRExist(task, result):
   try:
      task.check_detr_exist()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = []
      result['cmdInput'] = task.get('cmdInput')
      raise

def checkTicketState(task, result):
   try:
      task.check_detr_state()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = [task.get_related_log('detr')]
      result['cmdInput'] = task.get('cmdInput')
      raise

def checkTicketDate(task, result):
   try:
      task.check_detr_date()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = [task.get_related_log('detr')]
      result['cmdInput'] = task.get('cmdInput')
      raise

def checkRTExist(task, result):
   try:
      task.check_rt_exit()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = [task.get_related_log('detr')]
      result['cmdInput'] = task.get('cmdInput')
      raise

def checkRTMatch(task, result):
   try:
      task.check_rt_match()
   except analyError, e:
      result['cmdReturn'] = 'illegal'
      result['outputReturn'] = e.detail
      result['user'] = task.get('user')
      result['sid']  = task.get('sid')
      result['cmdTime'] = task.get('cmdTime')
      result['message'] = task.get('message')
      result['relatedlog'] = [task.get_related_log('detr'), task.get_related_log('rt')]
      result['cmdInput'] = task.get('cmdInput')
      raise

class tsuTask(baseTask):

   def __init__(self, adapter, data):
      super(baseTask, self).__init__(data)

      self.__dbAdapter = adapter
      self.__store = {}

   def __del__(self):
      pass

   def __prepare(self):
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'],
                                           'cmd':{'$regex':'detr', '$options':'I'}, # cmdName --> 'detr'
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )

      if cr is not None:
         detr = cr.next()
         self.append('detr', detr)
      else:
         return

      index = int(self.__data['index'])
      ticket = detr['ticket'][index - 1]

      cr = self.__dbAdapter.query('log', {'user':self.data['user'], 'pnr':ticket['pnr'],
                                          'cmd':{'$regex':'rt', '$options':'I'},
                                          'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      if cr is not None:
         rt = cr.next()
         self.append('rt', rt)

   def append(self, key, value):
      if self.__store[key] is not None:
         debug('key[%s] exist, value: %s, it will be replaced by new value: %s', key, self.__store[key], value)

      self.__store[key] = value

   def get_related_log(self, key):
      return self.__store[key];

   def check_forbbiden(self):
      if not self.__data['index'].isdigit():
         raise analyError('hit forbbiden element', self.data)

      if re.match(r'(\d{1}/[OFECVR]/)|NM', self.__data['state'], re.I):
         raise analyError('hit forbbiden element', self.data)

   def check_detr_exist(self):
      if self.__store['detr'] is not None:
         pass
      else:
         raise analyError('detr option is not done before!')

   def check_detr_state(self):
      detr = self.__store['detr']
      tickets = detr['ticket']
      if len(tickets) > 0:
         index = int(self.__data['index'])
         ticket = tickets[index - 1];
         state = ticket['state']
         if state.find('OPEN FOR USE'):
            pass
         elif state.find('USED'):
            raise analyError('ticket is used!')
         else:
            debug('cannot find \"OPEN FOR USE\" from ticket :%s', str(ticket))

   def check_detr_date(self):
      if self.__store['detr']['time'] < self.data['cmdTime']:
         raise analyError('ticket is expired!')
   """
   def __check_rt(self):
      cr = self.__dbAdapter.query('log', { 'user':self.data['user'], 'pnr':self.__detr_pnr
                                           'cmd':{'$regex':'rt', '$options':'I'},
                                           'cmdTime':{'$lt':self.data['cmdTime']}
                                         }
                                 )
      if cr is not None:
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
   """
   def check_rt_exist(self):
      rt = self.__store['rt']
      if rt is not None:
         pass
      else:
         raise analyError('rt option is not done before!')

   def check_rt_match(self):
      detr = self.__store['detr']
      ticket = tickets[self.__store['tid'] - 1];

      rt = self.__store['rt']
      ssrs = rt['ssrtkne']
      if len(tickets) > 0:
         for ssr in ssrs:
            if (ticket['tn'] == ssr['tn'] and
               ticket['comp'] == ssr['comp'] and ticket['plane'] == ssr['plane'] and
               ticket['magic'] == ssr['magic'] and ticket['date'] == ssr['date'] and
               ticket['idx'] == ssr['idx'] ):
               raise analyError('ticket is still valid', rt)
      else:
         pass


   def go(self):
      self.__prepare()
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
               'function':[ {'entry':'CheckValid', 'return':{'illegal':'ticket contais forbbiden flag!'}},
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
         debug('>>> current stage: %s', stageName)

         steps = stage['function']
         try:
            for step in steps:
               res = eval(funcMap[step['entry']][0])(self, result)
               if res == 'illegal':
                  # result contains all info of error
                  break
         except analyError,e:
            debug('catch an exception: %s', r.detail)
            break

      return result
