#! /usr/bin/python
# -*- coding:utf-8 -*-

import re

def debug(fmt, *args):
   """print log when debug
   """
   detail = fmt % (args)
   print(detail)

def get_command(log):
   cmd = None
   pattern = re.compile(r'>[, /:]*([\$\w]+)[\s:/\.,]', re.I)
   match = pattern.search(log)
   if match:
      cmd = match.group(1).upper()

   return cmd
