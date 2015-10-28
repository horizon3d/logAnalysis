#! /usr/bin/python

from client import client

if __name__ == '__main__':
   _client = client('localhost', 10086)
   _client.start('/home/tynia/coding/logAnalysis/client/2015_07_11_1.log')
