#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import re
from task import (baseTask, makeResult)
from error import (analyError, dbError)
from util.util import (debug, LogError, LogEvent)
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
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkDETRExist(task, result):
   try:
      task.check_detr_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkTicketState(task, result):
   try:
      task.check_detr_state()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      result['relatedlog'] = [task.at('detr')]
      raise

def checkTicketDate(task, result):
   try:
      task.check_detr_date()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      result['relatedlog'] = [task.at('detr')]
      raise

def checkRTExist(task, result):
   try:
      task.check_rt_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      result['relatedlog'] = [task.at('detr')]
      raise

def checkRTMatch(task, result):
   try:
      task.check_rt_match()
   except analyError, e:
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

      index = 0
      ticket = {}
      if self.get('index').isdigit():
         index = int(self.get('index'))
         for t in detr['ticket']:
            if index == t.get('idx'):
               ticket = t
               break
      else:
         return

      if ticket:
         if ticket['pnr'] is None or ticket['pnr'] == '':
            #debug('failed to get pnr in detr content')
            return
      else:
         #debug('cannot find any valid ticket in detr')
         return

      cr = self.dbAdapter.query('log', {'user':self.get('user'), 'pnr':ticket.get('pnr'), 'cmd':'RT', 'cmdTime':{'$lt':self.get('cmdTime')} }, {}, {'cmdTime':-1}, {} )
      rt = None
      try:
         rt = cr.next()
      except SDBEndOfCursor:
         return
      self.append('rt', rt)

   def check_forbbiden(self):
      if not self.get('index').isdigit():
         raise analyError('hit forbbiden element', self.data)

      if re.match(r'(\d{1}/[OFECVR]/)|NM', self.get('state'), re.I):
         raise analyError('hit forbbiden element', self.data)

   def check_detr_exist(self):
      if self.at('detr') is not None:
         pass
      else:
         raise analyError('detr option is not done before!')

   def check_detr_state(self):
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
               raise analyError('ticket is used!')
            else:
               debug('cannot find \"OPEN FOR USE\" from ticket :%s', str(ticket))
         else:
            raise analyError('no match ticket in detr', detr)
      else:
         raise analyError('no ticket in detr', detr)

   def check_detr_date(self):
      detr = self.at('detr')
      tickets = detr['ticket']
      if len(tickets) > 0:
         ticket = {}
         index = int(self.get('index'))
         for t in tickets:
            if index == t.get('idx'):
               ticket = t
               break
         if ticket['time'] < self.get('cmdTime'):
            raise analyError('ticket is expired!')
   
   def check_rt_exist(self):
      rt = self.at('rt')
      if rt is not None:
         pass
      else:
         raise analyError('rt option is not done before!')

   def check_rt_match(self):
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
               raise analyError('ticket is still valid', rt)
            else:
               pass
      else:
         pass

   def go(self):
      self.__prepare()
      self.map_stage()
      """
      tsuRule = {
         'ruleType':'CMDFLOW',
         'tragger':{
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
      for stageName in self.stage_dict:
         stage = self.rule['stage'][stageName]
         #debug('>>> current stage: %s', stageName)

         steps = stage['function']
         try:
            for step in steps:
               res = eval(funcMap[step['entry']])(self, result)
               if res == 'illegal':
                  # result contains all info of error
                  break
         except analyError,e:
            #debug('catch an exception: %s', r.detail)
            break

      return result