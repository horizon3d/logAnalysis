#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from client import client

if __name__ == '__main__':
   _client = client('localhost', 10086)
   _client.start('/home/tynia/coding/logAnalysis/client/2015_07_11_1.log')
