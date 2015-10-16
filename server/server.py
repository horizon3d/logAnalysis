#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import thread
from util import *
import connection

class server(object):
   def __init__(self, port):
      self.__sock = None

   def __del__(self):
      if self.__sock is not None:
         self.close()

   def close(self):
      self.__sock.close()
      self.__sock = None

   def run(self, port, maxconn):
      addr = ('', port)
      try:
         self.__sock = socket.socket(socket.AF_INET, socket.STREAM)
         self.__sock.bind(addr)
         self.__sock.listen(maxconn)
      except socket.error, e:
         __debug('error occurs on socket when listen, errno: %r', e)

      self.__run = True
      while self.__run:
         try:
            remote = self.__sock.accept()
         except socket.error,e:
            __debug('Failed to accept remote connection, error: %r', remote)
         conn = new connection(remote)
         thread.start_new_thread(thread_entry, conn.name())

   def stop(self):
      self.__run = False