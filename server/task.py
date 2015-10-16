#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *

class baseTask(object):

   def __init__(self, rule, data):
      self.__rule = rule
      self.__data = data
      self.__stage_dict = []

   def __del__(self):
      pass

   def get(self, key):
      return self.__data['key']
      
   def __map(self):
      stage = self.__rule['stage']
      for key in stage:
         self.__stage_dict.append(key)