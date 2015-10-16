#! /usr/bin/python
# -*- coding:utf-8 -*-

class analyError(Exception):
   def __init__(self, err, ev):
      self.__type = 'analysis error'
      self.__event = ev
      self.__error = err

      Exception.__init__(self, self.__error)


   def __del__(self):
      pass

   def __repr__(self):
      return '%s: %s, message: %s' % (self.__type, self.__error, str(self.__event))

   def __str__(self):
      return __repr__()

   @property
   def detail(self):
      return self.__error

class dbError(Exception):
   def __init__(self, code, err):
      self.__type = 'db error'
      self.__code = code
      self.__error = err
      Exception.__init__(self, self.__error)

   def __del__(self):
      pass

   def __repr__(self):
      return '%s: %s' % (self.__type, self.__detail())

   def __str__(self):
      return __repr__()

   def __detail(self):
      return 'Error code: %d, detail: %s' % (self.__code, self.__error)

   @property
   def code(self):
      return self.__code

   @property
   def detail(self):
      return self.__detail()
