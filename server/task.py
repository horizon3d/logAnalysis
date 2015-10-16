#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *

class baseTask(object):

   def __init__(self, data):
      self.__rule = None
      self.__data = data
      self.__stage_dict = []

   def __del__(self):
      pass
      
   def __map(self):
      stage = self.__rule['stage']
      for key in stage:
         self.__stage_dict.append(key)

   def set_rule(self, rule):
      self.__rule = rule

   def trag(self, cmdName):
      return cmdName == self.__data['cmd']