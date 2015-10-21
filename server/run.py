#! /usr/bin/python

from server import server

if __name__ == '__main__':
   _server = server(dbserver = 'localhost', svcname = 11810);
   _server.run(10086)
