#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from spliter import spliter
from helper import *
from connection import connection
from event import text_to_json

class client(object):
   def __init__(self, host, port):
      self.__conn = connection()
      self.__spilter = spliter()
      self.__connect(host, port)

   def __del__(self):
      pass

   def __connect(self, host, port):
      try:
         self.__conn.connect(host, port)
      except Exception, e:
         raise

   def parse(self, filename):
      user, sid, logs = self.__spilter.split(filename)
      for log in logs:
         event = text_to_json(log)
         if event is not None:
            event.append('user', user)
            event.append('sid', sid)

            self.__conn.send(event.get())
