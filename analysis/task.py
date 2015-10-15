#! /usr/bin/python

from analysis.tsu import tsu
from analysis.db import adapter
from analysis.util import *

__dbAdapter = None
__dbInited  = False

class task(object):
   """get rulers from table, generate rule and state-machine
   """

   def __init__(self, rule, ev):
      self.__rule = rule
      self.__event = ev
      self.__stage_dict = {}
      self.__call_dict = { 'prevCmdReturnSearch':'prevCmdReturnSearch', 'ulinkSearch':'ulinkSearch', 'outputResult':'outputResult'}

   def __del__(self):
      pass

   def __map(self):

      stage = self.__rule['stage']
      for key in stage:
         if key != 'Final':
            self.__stage_dict[key] = [ self.__call_dict[stage[key]['stageType']], stage[key]['returnCondition'] ]
         else:
            self.__stage_dict['Final'] = self.__call_dict['Final']

   def trag(self):
      pattern = re.compile(self.__rule['tragger']['cmd'], re.I)
      match = pattern.search(self.__event['cmd'])

      return match ? True : False

   def go(self):
      self.__map()

      lastStageName = '0'
      lastStageRet = ''
      stageName = '1'

      while True:
         stage = self.__rule['stage'][stageName]
         __debug('>>> current stage: %s', self.__stage_dict.get(stageName))
         res = eval(self.__stage_dict.get(stageName)[0])(lastStageName, lastStageRet, stageName, self.__event, self.__rule)
         lastStageName = stageName
         lastStageRet = res
         stageName = stage['returnCondition'][res].keys()[0]
         __debug('<<< lastStageName: %s, lastStageRet: %s, next stageName:%s', lastStageName, lastStageRet, stageName)

         if stageName == 'final':
            __debug('hit final state')
            break

      res = eval(self.__stage_dict.get(stageName)[0])(lastStageName, lastStageRet, stageName, self.__event, self.__rule)
      __debug('final result: %s', res)
