#! /usr/bin/python
# -*- coding:utf-8 -*-

import json
from tsuTask import tsuTask

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

def createTask(cmd, dbAdapter, rule, data):
   task = None
   if cmd == 'TSU':
      task = tsuTask(dbAdapter, rule, data)
   elif cmd == 'UU':
      task = uuTask(dbAdapter, rule, data)
   return task

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
