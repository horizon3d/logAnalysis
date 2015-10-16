#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from connection import connection
from spliter import spliter
from util import text_to_json

class client(object):
   def __init__(self, host, port):
      self.__conn = new connection()
      self.__spilter = new spliter()
      self.__connect(host, port)

   def __del__(self):
      pass

   def __connect(self, host, port):
      try:
         self.__conn.connect(host, port)
      except e:
         pass

   def parse(filename):
      user, sid, logs = self.__spilter.split(filename)
      for log in logs:
         event = text_to_json(log)
         event.append('user', user)
         event.append('sid', sid)
         
         self.__conn.send(event.get())