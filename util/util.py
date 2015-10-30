#! /usr/bin/python
# -*- coding:utf-8 -*-
import time
import re
import codecs

class ulog(object):
   def __init__(self):
      self.__name = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

   def __del__(self):
      pass

   @property
   def name(self):
      return self.__name

___ulog = ulog()

def console(fmt, *args):
   """print log when debug
   """
   detail = fmt % (args)
   print(detail)

def LogError(fmt, *args):
   detail = fmt % (args)
   ctx = 'Error:\r\n' + detail
   fd = None
   try:
      fd = codecs.open(___ulog.name, 'a', 'gbk')
      fd.write(ctx + '\n')
   except Exception, e:
      pass
   finally:
      if fd:
         fd.close()

def LogEvent(fmt, *args):
   detail = fmt % (args)
   ctx = 'Event:\r\n' + detail
   fd = None
   try:
      fd = codecs.open(___ulog.name, 'a', 'gbk')
      fd.write(ctx + '\n')
   except Exception, e:
      pass
   finally:
      if fd:
         fd.close()

def get_command(log):
   cmd = None
   pattern = re.compile(r'>[, /:]*([\$\w]+)[\s:/\.,]', re.I)
   match = pattern.search(log)
   if match:
      cmd = match.group(1).upper()

   return cmd

def trig(rule, cmdName):
   return cmdName == rule['trigger']['cmd']