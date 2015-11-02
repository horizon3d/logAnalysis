#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.abspath('.') + os.sep + '..'))
from util.util import (console, LogError, LogEvent)

class baseTask(object):

   def __init__(self, dbAdapter, rule, data):
      self.__dbAdapter = dbAdapter
      self.rule = rule
      self.__data = data
      self.stage_dict = []
      self.__store = {}

   def __del__(self):
      pass

   @property
   def data(self):
      return self.__data
      
   @property
   def dbAdapter(self):
      return self.__dbAdapter

   def append(self, key, value):
      if self.__store.get(key) is not None:
         console('key[%s] exist, value: %s, it will be replaced by new value: %s', key, self.__store[key], value)

      self.__store[key] = value

   def at(self, key):
      return self.__store.get(key);

   def get(self, key):
      return self.__data.get(key)
      
   def map_stage(self):
      stage = self.rule['stage']
      for key in stage:
         self.stage_dict.append(key)

   def go(self):
      console('run in base task, do nothing')

def makeResult(task, result):
   result['cmd'] = task.get('cmd')
   result['ruleName'] = task.rule.get('ruleName')
   result['user'] = task.get('user')
   result['sid']  = task.get('sid')
   result['cmdTime'] = task.get('cmdTime')
   result['message'] = task.get('message')
   result['cmdInput'] = task.get('cmdInput')
   result['cmdReturn'] = task.get('cmdReturn')
   result['relatedlog'] = []