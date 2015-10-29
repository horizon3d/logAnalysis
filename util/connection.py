#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import json
from util import (console, LogError, LogEvent)

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
      except Exception, e:
         LogError('Failed to connect to %s:%d', host, port)
         raise

   def send(self, data):
      if not data:
         LogEvent('try to send 0 byte(s)')
         return

      jdata   = json.dumps(data)
      length = len(jdata) + 8

      toSend = ('%8x' % length) + jdata
      sent = 0
      while sent < length:
         sendlen = self.__sock.send(toSend[sent:])
         sent += sendlen

   def recv(self):
      size = 0
      data = self.__sock.recv(8)
      if not data:
         raise socket.error('session closed')
      size = int(data, 16)
      need = size - 8
      data = ''
      while need > 0:
         rdata = self.__sock.recv(need)
         data += rdata
         need -= len(rdata)
      return json.loads(data)

   def close(self):
      if self.__sock is None:
         self.__sock.close()
         self.__sock = None


