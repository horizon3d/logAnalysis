#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.abspath('.') + os.sep + '..'))

import re
from task import (baseTask, makeResult)
from error import (analyError, dbError)
from util.util import (console, LogError, LogEvent)
from pysequoiadb.error import SDBEndOfCursor

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
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
      raise

def checkDETRExist(task, result):
   try:
      task.check_detr_exist()
   except analyError, e:
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
      raise

def checkTicketState(task, result):
   try:
      task.check_detr_state()
   except analyError, e:
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
         result['relatedlog'] = [task.at('detr')]
      raise

def checkTicketDate(task, result):
   try:
      task.check_detr_date()
   except analyError, e:
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
         result['relatedlog'] = [task.at('detr')]
      raise

def checkRTExist(task, result):
   try:
      task.check_rt_exist()
   except analyError, e:
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
         result['relatedlog'] = [task.at('detr')]
      raise

def checkRTMatch(task, result):
   try:
      task.check_rt_match()
   except analyError, e:
      if not e.ok:
         makeResult(task, result)
         result['errmsg'] = e.detail
         result['relatedlog'] = [task.at('detr'), task.at('rt')]
      raise

class tsuTask(baseTask):

   def __init__(self, dbAdapter, rule, data):
      baseTask.__init__(self, dbAdapter, rule, data)

   def __del__(self):
      pass

   def __prepare(self):
      cr = self.dbAdapter.query('log', { 'user':self.get('user'), 'cmd':'DETR', 'cmdTime':{'$lt':self.get('cmdTime')} }, {}, {'cmdTime':-1}, {})
      detr = None
      while True:
         try:
            detr = cr.next()
            if len(detr['ticket']) > 0:
               break
         except SDBEndOfCursor:
            return

      self.append('detr', detr)

      #cr = self.dbAdapter.query('log', {'user':self.get('user'), 'pnr':ticket.get('pnr'), 'cmd':'RT', 'cmdTime':{'$lt':self.get('cmdTime')} }, {}, {'cmdTime':-1}, {} )
      cr = self.dbAdapter.query('log', {'user':self.get('user'), 'cmd':'RT', 'cmdTime':{'$lt':self.get('cmdTime'), '$gt':detr['cmdTime']} }, {}, {}, {} )
      rt = None
      try:
         rt = cr.next()
      except SDBEndOfCursor:
         return

      self.append('rt', rt)

   def check_forbbiden(self):
      err = 'ticket contains forbbiden argument'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      if not self.get('index').isdigit():
         raise analyError(False, err, self.data)

      if re.match(r'(\d{1}/[OFECVR]/)|NM', self.get('state'), re.I):
         raise analyError(False, err, self.data)

      LogEvent('check forbbiden flag, ok')

   def check_detr_exist(self):
      err = 'detr option was not done before'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      if self.at('detr') is not None:
         pass
      else:
         raise analyError(False, err)

      LogEvent('detr exist, ok')

   def check_detr_state(self):

      err = 'detr context invalid'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      detr = self.at('detr')
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = {}
         index = int(self.get('index'))
         for t in tickets:
            if index == t.get('idx'):
               ticket = t
               break
         if ticket:
            state = ticket['state']
            if 'OPEN FOR USE' in state:
               pass
            elif 'USED' in state:
               raise analyError(False, 'ticket is used!') # can do tsu
            else:
               analyError(False, 'ticket state is not \"OPEN FOR USE\"')
         else:
            raise analyError(False, 'no match ticket in detr', detr) # can do tsu
      else:
         raise analyError(False, 'no match ticket in detr', detr)
      LogEvent('detr context, ok')

   def check_detr_date(self):
      err = 'detr ticket date invalid'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      detr = self.at('detr')
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = {}
         index = int(self.get('index'))
         for t in tickets:
            if index == t.get('idx'):
               ticket = t
               break
         if ticket['time'] is None:
            raise analyError(False, 'date:[%s] is invalid' % ticket['date'])
         if ticket['time'] < self.get('cmdTime'):
            LogEvent('ticket is expired, tsu ok')
            raise analyError(True, 'ticket is expired!')

      LogEvent('ticket date ok')
   
   def check_rt_exist(self):
      err = 'rt option was not done before'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      rt = self.at('rt')
      if rt is not None:
         pass
      else:
         raise analyError(False, err)

      LogEvent('rt exist, ok')

   def check_rt_match(self):

      err = 'tsu ticket in rt context'
      if len(self.illegal) > self.cur:
         err = self.illegal[self.cur]

      detr = self.at('detr')
      tickets = detr['ticket']
      ticket = {}
      if len(tickets) > 0:
         index = int(self.get('index'))
         for t in tickets:
            if index == t.get('idx'):
               ticket = t
               break

      rt = self.at('rt')
      ssrs = rt['ssrtkne']
      if len(tickets) > 0:
         for ssr in ssrs:
            if (detr['tn'] == ssr['tn'] and
               ticket['comp'] == ssr['comp'] and ticket['plane'] == ssr['plane'] and
               ticket['magic'] == ssr['magic'] and ticket['date'] == ssr['date'] and
               ticket['idx'] == int(ssr['idx']) ):
               raise analyError(False, err, rt)
               break
            else:
               pass

   def go(self):
      self.__prepare()
      self.map_stage()
      """
      tsuRule = {
         'ruleType':'CMDFLOW',
         'trigger':{
            'cmdReturn':'ACCEPTED',
            'cmd':'TSU',
            'traggerType':'cmd'
         },
         'ruleGroup':'1',
         'ruleName':'TSU test',
         'stage':{
            '1':{
               'function':[ {'entry':'CheckValid', 'return':{'illegal':'ticket contais forbbiden flag!'}},
                            {'entry':'CheckDETRExist', 'return':{'illegal':'detr option is not exist!'}},
                            {'entry':'CheckTicketState', 'return':{'illegal':'ticket is used!'}},
                            {'entry':'CheckTicketDate', 'return':{'illegal':'ticket is expired!'}} ],
               'cmdName':'DETR'
            },
            '2':{
               'function':[ {'entry':'CheckRTExist', 'return':{'illegal':'rt option is not exist!'}},
                            {'entry':'CheckRTMatch', 'return':{'illegal':'match a ticket that not used'}} ],
               'cmdName':'RT'
            }
         }
      }
      """

      result = {}
      self.cur = 0
      for stageName in self.stage_dict:
         stage = self.rule['stage'][stageName]
         steps = stage['function']
         try:
            for step in steps:
               res = eval(funcMap[step['entry']])(self, result)
               self.cur += 1
               if res == 'illegal':
                  # result contains all info of error
                  break
         except analyError,e:
            if not e.ok:
               LogError('catch an exception: %s', e.detail)
            break

      return result