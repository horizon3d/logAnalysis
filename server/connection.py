#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import json
from util import *

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
         debug('Failed to connect to %s:%d', host, port)
         debug('detail: %s', e)

   def send(self, data):
      if not data:
         debug('try to send 0 byte(s)')
         return

      jdata   = json.dumps(data)
      length = len(jdata) + 4

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
      datasize = size - 8
      recvlen = datasize
      rdata = ''
      while recvlen > 0:
         data = self.__sock.recv(recvlen)
         rdata += data
         recvlen -= len(data)

      return json.loads(rdata)

   def close(self):
      if self.__sock is None:
         self.__sock.close()
         self.__sock = None


