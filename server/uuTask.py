#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from task import baseTask

def checkULinkExist(task, result):
   try:
      task.check_ulink_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkULinkID(task, result):
   try:
      task.check_ulink_id()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOExist(task, result):
   try:
      task.check_mo_exist()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOLinkID(task, result):
   try:
      task.check_mo_id()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

def checkMOState(task, result):
   try:
      task.check_mo_state()
   except analyError, e:
      makeResult(task, result)
      result['errmsg'] = e.detail
      raise

class uuTask(baseTask):
   def __init__(self, dbAdapter, rule, data):
      baseTask.__init__(self, dbAdapter, rule, data)

   def __del__(self):
      pass

   def __prepare(self):
      pass

   def check_ulink_exist(self):
      pass

   def check_ulink_id(self):
      pass

   def check_mo_exist(self):
      pass

   def check_mo_id(self):
      pass

   def check_mo_state(self):
      pass



