#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from task import (baseTask, makeResult)

def checkULinkExist(task, result):
   try:
      task.check_ulink_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkULinkID(task, result):
   try:
      task.check_ulink_id()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOExist(task, result):
   try:
      task.check_mo_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOLinkID(task, result):
   try:
      task.check_mo_id()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOState(task, result):
   try:
      task.check_mo_state()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

class uuTask(baseTask):
   def __init__(self, dbAdapter, rule, data):
      baseTask.__init__(self, dbAdapter, rule, data)

   def __del__(self):
      pass

   def __prepare(self):
      user = self.get('user')
      # query from oracle
      sql = 'SELECT * FROM A'
      cursor = conn.execute(sql)
      rows = cursor.fetchall()
      records = []
      for row in rows:
         records.append(row)
      self.append('records', records)

      pid = self.get('pid')

      cr = self.dbAdapter.query('log', { 'user':self.get('user'), 'cmd':'MO', 'pid':pid, 'cmdTime':{'$lt':self.get('cmdTime')} }, {}, {'cmdTime':-1}, {})
      mo = None
      try:
         mo = cr.next()
      except SDBEndOfCursor:
         return
      self.append('mo', mo)

      cr = self.dbAdapter.query('log', { 'user':self.get('user'), 'cmd':'SEND', 'pid':pid, 'cmdTime':{'$lt':self.get('cmdTime')} }, {}, {'cmdTime':-1}, {})
      sendrec = None
      try:
         sendrec = cr.next()
      except SDBEndOfCursor:
         return
      self.append('send', sendrec)

   def check_ulink_exist(self):
      if self.at('records'):
         pass
      else:
         raise analyError('no ulink records done before uu option!')

   def check_ulink_id(self):
      pid = self.get('pid')
      records = self.at('records')
      for rec in records:
         if pid == rec.get('uid')
      pass

   def check_mo_exist(self):
      mo = self.at('mo')
      if mo:
         pass
      else:
         raise analyError('no mo option done!', self.data)

   def check_mo_id(self):
      pid = self.get('pid')
      mo = self.at('mo')
      moid = mo['id']
      if moid == pid:
         pass
      else:
         raise analyError('mo id is difference from the pid of uu')

   def check_mo_state(self):
      rec = self.at('send')
      message = rec['message']
      if 'FFP TRANSACTION IN PROGRESS, PLEASE DO FXE TO CANCEL OR EOT(@)' in message:
         pass
      else:
         raise analyError('user is unlocked before uu done')