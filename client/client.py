#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
import time
from helper import *
from connection import connection
from tailfile import tailfile
from event import text_to_json

def thread_entry(running, conn, tfile):
   debug('start new thread, begin to parse: [%s]', tfile.filename)
   while running:
      log = tfile.next_log()
      if log:
         event = text_to_json(log)
         if event is not None:
            event.append('user', tfile.user)
            event.append('sid', tfile.sid)
            try:
               conn.send(event.data())
            except socket.error, e:
               debug('send msg to server failed')
               break
      else:
         time.sleep(2)
   debug('end thread, end parsing [%s]', tfile.filename)

class client(object):
   def __init__(self, host, port):
      self.__conn = connection()
      self.__connect(host, port)
      self.__map = []
      self.__run = False

   def __del__(self):
      self.stop()
      self.__conn.close()

   def __connect(self, host, port):
      try:
         self.__conn.connect(host, port)
      except Exception, e:
         raise

   def __map_file(self, fArray):
      for one in fArray:
         tfile = tailfile(one)
         self.__map.append(tfile)

   @property
   def running(self):
      return self.__run

   def start(self, filename):
      #self.__map_file(fArray)
      tfile = tailfile(filename)
      self.__map.append(tfile)
      self.__run = True
      for t in self.__map:
         #thread.start_new_thread(thread_entry, (self.__run, self.__conn, t))
         thread_entry(self.__run, self.__conn, t)

   def stop(self):
      self.__run = False