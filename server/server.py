#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import thread
from util import *
from connection import connection
from db import adapter
from pysequoiadb.error import SDBEndOfCursor

def thread_entry(connName, conn, dbAdapter):
   debug('start new thread, from [%s]', connName)
   while True:
      try:
         data = conn.recv()
      except socket.error, e:
         #debug('remote session pipe closed, %r', e)
         break
      
      if data is not None:
         dbAdapter.upsert('log', data)

         task = assign_rule(dbAdapter, data)
         if task is not None:
            result = task.go()
            if result:
               dbAdapter.upsert('alarm', result)

   debug('end thread, from [%s]', connName)

def assign_rule(dbAdapter, data):

   if dbAdapter is None:
      debug('Error: db connector is not initialized')
      abort()
      return

   cond = {'userName':data['user']}
   cr = dbAdapter.query('user', cond)
   record = None

   try:
      record = cr.next()
   except SDBEndOfCursor, e:
      cr = dbAdapter.query('user', {'userName':'default'})

   try:
      record = cr.next()
   except SDBEndOfCursor, e:
      debug('cannot find any rule in user table')
      return

   if record is not None:
      usrGroups = record['ruleGroup']
      """
      tasks = []
      for userGroup in usrGroups:
         rules = __dbAdapter.query('rule', {'ruleGroup':userGroup})
         for rule in rules:
            if trag(rule, data['cmd'])
               task = createTask(data['cmd'], rule, data)
               tasks.append(task)
      return tasks
      """
      for userGroup in usrGroups:
         cr = dbAdapter.query('rule', {'ruleGroup':userGroup})
         rules = []
         while True:
            try:
               rule = cr.next()
               rules.append(rule)
            except SDBEndOfCursor:
               break

         for rule in rules:
            if trag(rule, data['cmd']):
               task = createTask(data['cmd'], dbAdapter, rule, data)
               return task

def execTask(dbAdapter, task):
   ret = task.go()
   if ret:
      dbAdapter.upsert('alarm', ret)

class server(object):
   def __init__(self, dbserver = 'localhost', svnname = 11810):
      self.__sock = None
      self.__dbAdapter = adapter(host = dbserver, port = svnname)

   def __del__(self):
      if self.__sock is not None:
         self.close()

   def close(self):
      self.__sock.close()
      self.__sock = None

   def run(self, port, maxconn = 5):
      addr = ('', port)
      try:
         self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.__sock.bind(addr)
         self.__sock.listen(maxconn)
      except socket.error, e:
         debug('error occurs on socket when listen, errno: %r', e)

      self.__run = True
      addr = ('none', 0)
      while self.__run:
         try:
            remote, addr = self.__sock.accept()
         except socket.error,e:
            debug('Failed to accept remote connection, error: %s', e)
         debug('received a connection from %s:%d', addr[0], addr[1])
         conn = connection(remote)
         thread.start_new_thread(thread_entry, (conn.name(), conn, self.__dbAdapter))

   def stop(self):
      self.__run = False
