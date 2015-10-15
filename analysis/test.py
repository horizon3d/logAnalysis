#! /usr/bin/python

from util import *
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
"""
logs = []
logdetr = '---------------------------User: chengchen   SID: 55---------------------------\r\n2015 September 22, Tuesday, 16:54:57\r\n>detr tn  9999686012042 \r\n DETR:TN  9999686012042                                                        \r\nISSUED BY: AIR CHINA                 ORG/DST: BJS/SHA                 BSP-I     \r\nE/R: 9BJ10G0C/NONEND                                                            \r\nTOUR CODE: X9BJ10G0C                                         RECEIPT PRINTED  \r\nPASSENGER: DONG/XUEMIN                                                          \r\nEXCH:                               CONJ TKT:                                   \r\nO FM:1PEK CA     995  Z 08SEP 1500 OK ZXAP7H/NA  08SEP5/08SEP5 2PC USED/FLOWN   \r\n     T3-- RL:NB416S  /HS3N8R1E BG:2/43K BN:149                                  \r\nO TO:2IAH CA     996  Z 25SEP 0100 OK ZWAP7H/NA  25SEP5/25SEP5 2PC OPEN FOR USE \r\n     --T3 RL:NB416S  /HS3N8R1E                                                  \r\nX TO:3PEK CA    1831  F 26SEP 0730 OK F/NA       26SEP5/26SEP5 2PC OPEN FOR USE \r\n     T3T2 RL:NB416S  /HS3N8R1E                                                 +'
logrt = '2015 September 22, Tuesday, 16:55:11\r\n>RT NB416S\r\n  **ELECTRONIC TICKET PNR**                                                     \r\n 1.DONG/XUEMIN 2.JIE/LINPING NB416S                                             \r\n 3.  CA996  Z1  FR25SEP  IAHPEK RR2   0100 0450+1    E --T3                     \r\n 4.  CA1831 F1  SA26SEP  PEKSHA RR2   0730 0940      E T3T2                     \r\n 5.T BJS/PEK/T 010-85227818/CHINA INTERNATIONAL TRAVEL SERVICE                  \r\n 6.T BJS//YE CHANGJIANG                                                         \r\n 7.SSR TKNE CA HK1 PEKIAH 995 Z08SEP 9999686012042/1/P1                         \r\n 8.SSR TKNE CA HK1 PEKIAH 995 Z08SEP 9999686012043/1/P2                         \r\n 9.SSR TKNE CA HK1 IAHPEK 996 Z25SEP 9999686012043/2/P2                         \r\n10.SSR TKNE CA HK1 PEKSHA 1831 F26SEP 9999686012043/3/P2                        \r\n11.SSR TKNE CA HK1 IAHPEK 996 Z25SEP 9999686012042/2/P1                         \r\n12.SSR TKNE CA HK1 PEKSHA 1831 F26SEP 9999686012042/3/P1                       +'
logtsu = logtxt = "2015 September 22, Tuesday, 16:55:18\r\n>TSU 2/OPEN\r\nACCEPTED"

if __name__ == '__main__':

   for item in logs:
      e = insert_to_db(item)
      #e.go()
"""
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
   """