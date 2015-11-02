#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('.') + os.sep + '..'))
from util.util import (LogError, LogEvent)
from pysequoiadb import client
from pysequoiadb.error import SDBBaseError

class adapter(object):

   def __init__(self, host = 'localhost', port = 11810, user = '', password = '', csname = 'zhx'):
      self.__initialize(csname, host, port, user, password)
      self.__cls = {}

   def __del__(self):
      self.__cc.disconnect()

   def __repr__(self):
      return '%s, %s' % (self.__cc, self.__cs)

   def __initialize(self, csname, host, port, user, password):
      try:
         self.__cc = client(host, port, user, password)
         self.__cs = self.__cc[csname]
      except SDBBaseError, e:
         LogError('Error: %s, program exit', e.detail)
         exit(1)

   def upsert(self, clname, record):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         LogEvent('access to %s', self.__cls.get(clname))

      try:
         cl = self.__cls.get(clname)
         cl.upsert({'$set':record}, condition = {'cmdTime':record['cmdTime'], 'user':record['user'], 'sid':record['sid'], 'cmd':record['cmd']})
      except SDBBaseError, e:
         LogError('Error: Failed to insert record to collection: %s, detail: %s, event: %s', clname, e.detail, str(record))
         return

   def query(self, clname, cond = {}, selector = {}, sort = {}, hint = {}):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         LogEvent('access to %s', self.__cls.get(clname))

      cl = self.__cls.get(clname)
      if cl is None:
         LogError('%s.%s not exist', self.__cs.get_collection_space_name(), clname)
      return cl.query(condition = cond, selector = selector, order_by = sort, hint = hint)

   def insert(self, clname, record):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         LogEvent('access to %s', self.__cls.get(clname))

      cl = self.__cls.get(clname)
      if cl is None:
         LogError('%s.%s not exist', self.__cs.get_collection_space_name(), clname)
      return cl.insert(record)