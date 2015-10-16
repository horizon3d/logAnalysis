#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import json
from helper import *

class connection(object):
   def __init__(self, sock = None):
      self.__sock = sock

   def __del__(self):
      pass

   def name(self):
      if self.__sock is None:
         return 'Not connected'
      return '%s:%d' % self.__sock.getpeername()

   def connect(self, host, port):
      if self.__sock is not None:
         self.close()

      addr = (host, port)
      try:
         self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.__sock.connect(addr)
      except socket.error, e:
         pass

   def send(self, data):
      if not data:
         __debug('try to send 0 byte(s)')
         return

      jdata   = json.dumps(data)
      length = len(data) + 4

      toSend = '%4d' % length + jdata
      while sent < length:
         sendlen = self.__sock.send(toSend[sent:])
         sent += sendlen
      __debug('send %d bytes: %s', str(data))

   def recv(self):
      size = int(self.__sock.recv(4))
      jdata = self.__sock.recv(size - 4)
      data = json.loads(jdate)
      __debug('received %d bytes: %s', str(data))
      return data

   def close(self):
      self.__sock.close()
      self.__sock = None


