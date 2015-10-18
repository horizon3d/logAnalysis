#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *

class baseTask(object):

   def __init__(self, dbAdapter, rule, data):
      self.__dbAdapter = dbAdapter
      self.rule = rule
      self.__data = data
      self.stage_dict = []

   def __del__(self):
      pass

   @property
   def data(self):
      return self.__data
      
   @property
   def dbAdapter(self):
      return self.__dbAdapter

   def get(self, key):
      return self.__data.get(key)
      
   def map_stage(self):
      stage = self.rule['stage']
      for key in stage:
         self.stage_dict.append(key)