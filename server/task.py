#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *

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
         debug('key[%s] exist, value: %s, it will be replaced by new value: %s', key, self.__store[key], value)

      self.__store[key] = value

   def at(self, key):
      return self.__store.get(key);

   def get(self, key):
      return self.__data.get(key)
      
   def map_stage(self):
      stage = self.rule['stage']
      for key in stage:
         self.stage_dict.append(key)