#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from connection import connection
from spliter import spliter
from util import text_to_json

class client(object):
   def __init__(self, host, port):
      self.__conn = new connection()
      self.__conn.conect(host, port)
      
      self.__spilter = new spliter()

   def __del__(self):
      pass

   def __split(self, filename):
      return self.__spilter.spilt(filename)

   def parse(filename):

      logs = self.__split(filename)
      for log in logs:
         event = text_to_json(log)
         self.__conn.send(event.get())