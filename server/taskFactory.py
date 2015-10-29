#! /usr/bin/python
# -*- coding:utf-8 -*-

from tsuTask import tsuTask

def createTask(cmd, dbAdapter, rule, data):
   task = None
   if cmd == 'TSU':
      if 'ACCEPTED' in data['cmdReturn']:
         task = tsuTask(dbAdapter, rule, data)
   #elif cmd == 'UU':
      #task = uuTask(dbAdapter, rule, data)
   return task