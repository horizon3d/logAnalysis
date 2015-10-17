#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import thread
from util import *
from connection import connection

class server(object):
   def __init__(self):
      self.__sock = None

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
         thread.start_new_thread(thread_entry, (conn.name(), conn))

   def stop(self):
      self.__run = False
