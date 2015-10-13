#! /usr/bin/python

class const:
   class constError(typeError):
      pass
   def __setattr__(self, name, value):
      if self.__dict__.has_key(name):
         raise self.constError(("try to rebuild key:%s") % name)
      self.__dict__[name] = value

import sys
sys.modules[__name__] = const()

def get_version():
   ver = '0.0.1'
   return ver