#! /usr/bin/python
# -*- coding:utf-8 -*-

class uuTask(baseTask):
   def __init__(self, dbAdapter, rule, data):
      baseTask.__init__(self, dbAdapter, rule, data)

   def __del__(self):
      pass

