#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *
from pysequoiadb import client
from pysequoiadb.error import SDBBaseError

class adapter(object):

   def __init__(self, csname = 'zhx', host = 'localhost', port = 11810, user = '', password = ''):
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
         debug('Error: %s', e.detail)
         debug('exit')
         exit(1)

   def upsert(self, clname, record):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         debug('access to %s', self.__cls.get(clname))

      try:
         cl = self.__cls.get(clname)
         cl.upsert({'$set':record}, condition = {'cmdTime':record['cmdTime'], 'user':record['user'], 'sid':record['sid'], 'cmd':record['cmd']})
      except SDBBaseError, e:
         debug('Error: Failed to insert record to collection: %s, event: %s', clname, str(record))
         debug('%s', e.detail)
         return

      debug('insert a record into collection: %s', clname)
      debug('record: %s', str(record))
      debug('\r\n\r\n')

   def query(self, clname, cond = {}, selector = {}, sort = {}, hint = {}):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         debug('access to %s', self.__cls.get(clname))

      cl = self.__cls.get(clname)
      if cl is None:
         debug('%s.%s not exist', self.__cs.get_collection_space_name(), clname)
      return cl.query(condition = cond, selector = selector, order_by = sort, hint = hint)

   def insert(self, clname, record):

      if self.__cls.get(clname) is None:
         self.__cls[clname] = self.__cs[clname]
         debug('access to %s', self.__cls.get(clname))

      cl = self.__cls.get(clname)
      if cl is None:
         debug('%s.%s not exist', self.__cs.get_collection_space_name(), clname)
      return cl.insert(record)