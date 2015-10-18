#! /usr/bin/python
# -*- coding:utf-8 -*-

import json
from tsuTask import tsuTask
from db import adapter
import re
import socket

__dbAdapter = adapter()

userDict = {}
def load():
   fp = open('user.csv', 'r')
   for line in fp.readlines():
      cell = line.split(',')
      if not cell[7] == '':
         userDict[cell[7]] = cell[3]

def debug(fmt, *args):
   """print log when debug
   """
   detail = fmt % (args)
   print(detail)

def trag(rule, cmdName):
   return cmdName == rule['tragger']['cmd']

def createTask(cmd, rule, data):
   if cmd == 'TSU':
      task = tsuTask(rule, data)

def assign_rule(data):

   if __dbAdapter is None:
      debug('Error: db connector is not initialized')
      abort()
      return

   cond = {'userName':data['user']}
   cr = __dbAdapter.query('user', cond)
   if cr is None:
      cr = __dbAdapter.query('user', {'userName':'default'}})

   if cr is not None:
      rec = cr.next()
      usrGroups = rec['ruleGroup']
      """
      tasks = []
      for userGroup in usrGroups:
         rules = __dbAdapter.query('rule', {'ruleGroup':userGroup})
         for rule in rules:
            if trag(rule, data['cmd'])
               task = createTask(data['cmd'], rule, data)
               tasks.append(task)
      return tasks
      """
      for userGroup in usrGroups:
         rules = __dbAdapter.query('rule', {'ruleGroup':userGroup})
         for rule in rules:
            if trag(rule, data['cmd']):
               task = createTask(data['cmd'], rule, data)
               return task

def execTask(task):
   ret = task.go()
   if not ret['result']:
      __dbAdapter.insert('alarm', ret)

def thread_entry(connName, conn):
   debug('start new thread, from [%s]', connName)
   while True:
      try:
         data = conn.recv()
      except socket.error, e:
         #debug('socket error occurs when receiving packet: %r', e)
         break
      
      if data is not None:
         print(data)
         debug('\r\n\r\n')
         __dbAdapter.insert('log', data)

         assign_rule(task)
         if task is not None:
            result = task.go()
            if not result['outputResult']:
               __dbAdapter.insert('alarm', ret)

   debug('end thread, from [%s]', connName)

"""
def ulinkSearch(lastStage, lastStageRet, stageName, ev, rule):
   load()

   stage = rule['stage'][stageName]
   returnCondition = stage['returnCondition']

   conn = cx_Oracle.connect('travelsky_ulink', 'travelsky_ulink', '10.6.184.143:1525/Com4m')

   try:
      ulinkid = userDict[event['user']]
   except:
      return 'illegal'

   sql = '''select a.eve_id,
      b.use_ali_id,
      d.sta_dat,
      d.end_dat,
      a.Eve_Des,
      a.Eve_Detail_Des,
      a.SOLUTION,
      from c_eve a,
      c_use b,
      c_tas d,
      c_tas_cha e,
      c_cha f,
      c_cus_bas g
      wherea.accept_user_id = b.use_id
      and b.use_ali_id = \'''' + ulinkid + ''''
      and a.tas_id = d.tas_id
      and a.accept_time > \'''' + strftime("%Y-%m-%d", localtime(time())) + ''' 00:00'
      and d.tas_id = e.tas_id
      and e.cha_id = f.cha_id
      and a.CUS_ALI_ID = g.CUS_ALI_ID
      order by e.eve_id desc'''

   cursor = conn.execute(sql)
   rows = cursor.fetchall()

   if len(rows):
      return 'legal'
   else:
      return 'illegal'
"""
