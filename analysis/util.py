#! /usr/bin/python

from parser import parser
from tsu import tsu
import json
from event import event
from task import task
import re

def __debug(fmt, *args):
   """print log when debug
   """
   detail = fmt % (args)
   print detail

def text_to_json(log):

   cmd_pattern = re.compile(r'>([a-zA-Z]+) ', re.I)
   obj = cmd_pattern.search(log)
   if obj:
      cmd = obj.group(1)

   if cmd == 'tsu':
      e = new tsu(None, log)
   if cmd == 'detr':
      e = new detr(log)
   if cmd == 'rt':
      e = new rt(log)

   return e

userDict = {}
def load():
   fp = open('user.csv', 'r')
   for line in fp.readlines():
      cell = line.split(',')
      if not cell[7] == '':
         userDict[cell[7]] = cell[3]

__dbAdapter = None
__dbInited  = False

def insert_to_db(log):

   #if !__dbInited and __dbAdapter is None:
   #   __dbAdapter = new adapter()
   #   __dbInited  = True

   event = text_to_json(log)

   self.__dbAdapter.insert('log', event.data)
"""
   if event.data['cmd'].contains('tsu'):
      tsuRule = tsuParser()
      tsuRule.setBase(__parser)
      tsuRule.go(log)
   elif event.data['cmd'].contains('uu'):
      pass
   elif event.data['cmd'].contains('rt'):
      # TODO:
      pass
   elif event.data['cmd'].contains('da'):
      # TODO:
      pass
   elif event.data['cmd'].contains('rt'):
      # TODO:
      pass
"""
   return event;

def assign_rules(ev):

   if __dbAdapter is None:
      __debug('Error: db connector is not initialized')
      abort()
      return

   cond = {'userName':ev['user']}
   if __dbAdapter.query('user', cond).count() > 0:
      cr = __dbAdapter.query('user', cond)
   else:
      cr = __dbAdapter.query('user', {'userName':'default'}})

   if cr not None:
      rec = cr.next()
      usrGroups = rec['ruleGroups']

   tasks = []
   for userGroup in usrGroups:
      rules = __dbAdapter.query('rule', {'ruleGroup':userGroup})
      for rule in rules:
         ruleTask = new task(rule, ev)
         if ruleTask.trag():
            tasks.append(ruleTask)

   return tasks

def exec_rule(task):

   if __dbAdapter is None:
      __debug('Error: db connector is not initialized')
      return

   ret = task.go()
   if !ret['result']:
      __dbAdapter.insert('alarm', ret)

def get_str(ev, matcher):
   ctx = ev['message']
   result = []

   for (ms, rs) in matcher.items():
      pattern = re.compile(ms)
      match = pattern.search(ctx)
      if match:
         result.append(rs)

   if len(result):
      return result[0]
   else:
      return 'Error'

def get_date(ev, dateCmp):

   ctx = ev['message']
   cmdTime = ev['cmdTime']
   month = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
   pattern = re.compile(r'(\d{2})([A-Z]{3})(\d{4})')
   match = pattern.search(ctx)
   mon = month[match.group(2)]
   day = match.group(1)
   time = match.group(3)
   year = strftime('%Y', gmtime())
   ts = mktime(strptime(year+ ' ' + mon + ' ' + day + time[0:2] + ':' + time[2:4] + ':' + ':00', '%Y %m %d %H:%M:%S'))

   if ts < cmdTime:
      return dateCmp['lt']
   else:
      return dataCmp['gt']

def prevCmdReturnSearch(lastStage, lastStageRet, stageName, ev, rule):

   stage = rule['stage'][stageName]
   res = 'Error'
   parameter = stage['parameter']
   returnCond = stage['returnCondition']
   cmdName = stage['cmdName']
   funcDict = {'strMatch':get_str, 'dateCmp':get_date}

   resultCursor = __dbAdapter.query('log', {'user':ev['user'], 'cmd':{'$regex':cmdName, '$options':'I'}, 'cmdTime':{'$lt':ev['cmdTime']}}).sort([('cmdTime', -1)]).limit(1)

   if resultCursor.count():
      for (funcType, inPara) in parameter.items():
         res = funcDict.get(funcType)(resultCursor[0], inPara)

   return res

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

def outputResult(lastStage, lastStageRet, stageName, ev, rule):

   stage = rule['stage'][stageName]
   returnCondition = stage['returnCondition']
   lastReturnCondition = rule['stage'][lastStage]['returnCondition'][lastStageRet][stageName]

   outputReturn = rule['stage'][stageName]['returnCondition'][lastReturnCondition[0]]

   pattern.re.compile(r'\[([\w]+)\]')

   while True:
      match = pattern.search(outputReturn)
      if match:
         res = str(match.group(1))

         if res == 'cmdTime':
            outputReturn = outputReturn.replace('[' + res + ']', strftime("%Y-%m-%d %H:%M:%S", localtime(ev[res])))
         elif res == 'ruleName':
            outputReturn = outputReturn.replace('[' + res + ']', rule[res])
         elif res == 'lastStageRet':
            outputReturn = outputReturn.replace('[' + res + ']', lastReturnCondition[1])
         else:
            outputReturn = outputReturn.replace('[' + res + ']', ev[res])

      else:
         break

   cr = __dbAdapter.query('output', {'cmdTime':ev['cmdTime'], 'cmd':ev['cmd'], 'user':ev['user']})

   doc = 
   {
      'user':ev['user'],
      'sid':ev['sid'],
      'message':ev['message'],
      'cmdInput':ev['cmdInput'],
      'cmdReturn':ev['cmdReturn'],
      'cmdTime':ev['cmdTime'],
      'lastStageReturn':lastReturnCondition[1],
      'outputResult':outputResult
   }

   __dbAdapter.insert('output', doc)

   return (lastReturnCondition[0], outputResult+'\n')

def finalAction(finalType, finalInfo, host, path, timestamp):

   cr = __dbAdapter.query('log', {'path':path, 'host':host, 'timestamp':timestamp})
   for item in cr:
      cmd = item['cmd']
      if finalType == 'Error':
         __debug('Error: %s, path: %s, host: %s, cmd: %s', finalInfo, path, host, cmd)
      elif finalType == 'Info':
         __debug('Information: %s, path: %s, host: %s, cmd: %s', finalInfo, path, host, cmd)