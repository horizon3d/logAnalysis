#! /usr/bin/python

import re
import json

class parser(object):

   def __init__(self):
      self.path = ''
      self.__set_default()

   def __del__(self):
      pass

   def __set_default(self):
      self.__reg_usr_sid = re.compile(r'[-]+User: ([0-9a-zA-Z]+)[ ]+SID: (\d+)[-]+')
      self.__reg_time   = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)')
      self.__reg_cmd    = re.compile(r'>([\w /,;]+[\w])[\s]*\n([\w /,;]+[\w])')
      self.__reg_cmdrtn = re.compile(r'>[\w /,;]+[\w][\s]*\n(.*)')
      self.__reg_flag   = re.compile(r'\+[\s]*&')

   def members(self):
      return ['user', 'time', 'cmd', 'cmdReturn', 'flag']

   def parse(self, log):
      self.__log_content = log
      self.user, self.sid, self.fileHeader = self.__get_usr()
      self.time = self.__get_time()
      self.cmd  = self.__get_cmd()
      self.cmdReturn = self.__get_return()
      self.flag = self.__get_flag()


   def set_regex(self, **kwargs):

      if kwargs['user'] not None:
         self.__reg_user = re.compile(kwargs['user'])
      if kwargs['time'] not None:
         self.__reg_time = re.compile(kwargs['time'])
      if kwargs['cmd'] not None:
         self.__reg_cmd    = re.compile(kwargs['cmd'])
      if kwargs['cmdReturn'] not None:
         self.__reg_cmdrtn = re.compile(kwargs['cmdReturn'])
      if kwargs['flag'] not None:
         self.__reg_flag = re.compile(kwargs['flag'])

   def reset_regex(self):
      self.__set_default()

   def __get_time(self):
      month = { 'January':'01', 'February':'02', 'March':'03',
   'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08',
   'September':'09', 'October':'10', 'November':'11', 'December':'12' }
      match = self.__reg_time.search(self.__log_content)
      if match:
         otime = match.group().split(',')
         ymd = otime[0]
         for (k, v) in month.items():
            ymd = ymd.replace(k,v)
      return time.mktime(time.strptime((ymd + otime[2]), '%Y %m %d %H %M %S'))

   def __get_cmd(self):
      match = self.__reg_cmd.search(self.__log_content)
      if match:
         cmd1 = match.group(1)
         cmd2 = match.group(2)
         self.cmdInput = cmd1

         cmp1 = re.split('[:/, ]', cmd1)[0].upper()
         cmp2 = re.split('[:/, ]', cmd2[1:])[0].upper()

         if cmd1 == cmd2:
            cmd = cmd2[1:]
         else:
            cmd = cmd1.upper()
         __debug('command: %s', cmd)
      return cmd

      def __get_usr(self):
         match = self.__reg_usr_sid.search(self.__log_content)
         if match:
            user = match.group(1)
            sid = match.group(2)
            file_header = True
         else:
            db = client()
            db = cc.zhx
            cr = db.zhx.find({'fileHeader':True, 'path': self.path})
            if cr.count() > 0:
               rec = cursor.next()
               user = rec['user']
               sid = rec['sid']
            file_header = False
            __debug('user: %s, sid: %s', user, sid)
         return user, sid, file_header

      def __get_return(self):
         if self.__reg_time.match(self.__log_content):
            match = self.__reg_cmdrtn.search(self.__log_content)
            if match:
               rtn = match.group(1)
            __debug('return: %s', rtn)
         return rtn

      def __get_flag(self):
         match = self.__reg_flag.search(self.__log_content)
         if match:
            flag = False
         else:
            flag = True
         return flag
