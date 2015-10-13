#! /usr/bin/python

from analysis.util import *
from pysequoiadb import client

class adapter(object):

   def __init__(self, csname = 'zhx', host, port, user, password):
      self.__initialize()

   def __del__(self):
      pass
   def __initialize(self):
      try:
         self.__cc = client(host, port, user, password)
         self.__cs = self.__cc[csname]
      except e:
         debug('Error: %s', e.detail)


   def insert(self, clname, ev):

      try:
         self.__cs[clname].upsert(log, condition = {'cmdTime':ev.data['cmdTime'], 'user':ev.data['user'], 'sid':ev.data['sid'], 'cmd':ev.data['cmd']})
      except:
         __debug('Error: Failed to insert event to collection: %s, event: %s', clname, ev)
         return

      __debug('insert a record into collection: %s, record: %s', clname, ev)

   def query(self, clname, cond = None, selector = None, sort = None, hint = None):

      self.__cs[clname].query(cond, selector, sort, hint)
