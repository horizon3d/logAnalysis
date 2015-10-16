#! /usr/bin/python
# -*- coding:utf-8 -*-

import json
from event import (event, tsu, detr, rt)
import re

def __debug(fmt, *args):
   """print log when debug
   """
   detail = fmt % (args)
   print(detail)

def get_command(log):
   cmd = None
   pattern = re.compile(r'>[, /:]*([\w]+)[\s:/,]', re.I)
   match = pattern.search(log)
   if match:
      cmd = match.group(1).upper()

   return cmd

def text_to_json(log):
   cmd = get_command(log)
   e = None
   if cmd == 'TSU':
      e = tsu()
   elif cmd == 'DETR':
      e = detr()
   elif cmd == 'RT':
      e = rt()
   else:
      e = event(cmd)
   if e is not None:
      e.to_json(log)

   return e
