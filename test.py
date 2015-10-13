#! /usr/bin/python

import analysis
from analysis.ruler import ruler
from analysis.util import *

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
         'stageType':'prevCmdReturnSearch', 'parameter':{'strMatch':{'OPEN FOR USE':'legal', 'USED':'illegal'} },
         'returnCondition':{'illegal':{'final':['Error':, 'ticket is used!']}, 'legal':{'2':[]}},
         'cmdName':'DETR'
      }
      '2':{
         'stageType':'prevCmdReturnSearch', 'parameter':{'dateCmp':{'lt':'illegal', 'gt':'legal'}},
         'returnCondition':{'illegal':{'final':['Error', 'expired']}, 'legal':{'final':['Info':'normal action']}},
         'cmdName':'DETR'

      }
      'final':{'stageType':'outResult',
         'returnCondition':{
            'Info' :'[cmdTime] User:[user] SID:[sid]: \"[cmdInput]\" is legal! Match \"[ruleName]\"',
            'Error':'[cmdTime] User:[user] SID:[sid]: \"[cmdInput]\" is illegal! Don\'t match \"[ruleName]\". Because [lastStageReturn].'}
      }
   }
}

if __name__ == '__main__':

   logtxt = "2015 September 22, Tuesday, 16:51:55\r\n>TSU 1/OPEN\r\nACCEPTED"

   ruler = new ruler()
   ret = ruler.go(logtxt)
   if !ret['result']:
      alert()

   # zhx codes
   sc = SparkContext(appName='ZHX')
   ssc = StreamingContext(sc, 15)

   lines = ssc.textFilesStream('/tmp/log')

   # insert
   mapToDB = line.map(insert_to_db)
   counts = mapToDB.count()
   counts.pprint()

   # analysis
   mapToAnalyze = mapToDB.flatMap(assign_rules)
   counts = mapToAnalyze.count()
   counts.pprint()

   # for statistics?
   analyOutput = mapToAnalyze.map(exec_rule)
   output = analyOutput.reduce(lamada a, b: a+b)
   output.pprint()

   ssc.start()
   ssc.awaitTermiation()