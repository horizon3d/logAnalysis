#! /usr/bin/python
# -*- coding:utf-8 -*-

from util import *
from pysequoiadb import client

class adapter(object):

   def __init__(self, csname = 'zhx', host, port, user, password):
      self.__initialize(csname, host, port, user, password)
      self.__cls = {}

   def __del__(self):
      self.__cc.disconnect

   def __initialize(self, csname, host, port, user, password):
      try:
         self.__cc = client(host, port, user, password)
         self.__cs = self.__cc[csname]
      except e:
         debug('Error: %s', e.detail)
         debug('exit')
         exit(1)

   def insert(self, clname, record):

      if self.__cls[clname] is None:
         self.__cls[clname] = self.__cs[clname]

      try:
         self.__cls[clname].upsert(log, condition = {'cmdTime':record['cmdTime'], 'user':record['user'], 'sid':record['sid'], 'cmd':record['cmd']})
      except e:
         debug('Error: Failed to insert event to collection: %s, event: %s', clname, str(record))
         debug('%s', e.detail)
         return

      debug('insert a record into collection: %s, record: %s', clname, str(record))

   def query(self, clname, cond = None, selector = None, sort = None, hint = None):

      self.__cls[clname].query(cond, selector, sort, hint)
