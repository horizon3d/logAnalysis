#! /usr/bin/python

from server import server

if __name__ == '__main__':
   _server = server();
   _server.run(10086)
