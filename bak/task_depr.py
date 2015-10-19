#! /usr/bin/python
# -*- coding:utf-8 -*-

from tsu import tsu
from db import adapter
from util import *

__dbAdapter = None
__dbInited  = False

class task(object):
   """get rulers from table, generate rule and state-machine
   """

   def __init__(self, rule, data):
      self.__rule = rule
      self.__data = data

   def __del__(self):
      pass

   def __map(self):

      stage = self.__rule['stage']
      for key in stage:
         self.__stage_dict.append(key)

   def trag(self, cmdName):
      return self.__data['cmd'] == self.__rule['tragger']['cmd']

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
