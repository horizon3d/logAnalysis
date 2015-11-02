#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.abspath('.') + os.sep + '..'))

from server import server

if __name__ == '__main__':
   _server = server(dbserver = 'localhost', svcname = 11810);
   _server.run(10086)
