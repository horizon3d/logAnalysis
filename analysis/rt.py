#! /usr/bin/python

import re
from analysis.event import event

class rt(event):

   def __init__(self, log):
      super(event, self).__init__()
      self.convert(log)

      self.__cmd_pattern = re.compile(r'>rt ([\w]+)', re.I)
      self.data['cmd'] = 'rt'
      self.__flat(log)

   def __del__(self):
      pass

   def __flat(self, log):
      pnr_pattern = re.compile(r'>rt ([\w]+)', re.I)
      obj = pnr_pattern.search(log)
      if obj:
         self.data['pnr'] = obj.group(1)
      ssr_pattern = re.compile(r'SSR TKNE ([\w]+) [\w]+ ([\d]+) ([A-Z]])([\d{2}\w{3}]+) ([\d]+)/(\d{1})/[\w]+', re.I)
      obj = ssr_pattern.findall(log)
      self.data['ssktkne'] = []
      ssr = {}
      for item in obj:
         ssr['comp'] = item[0]
         ssr['plane'] = item[1]
         ssr['magic'] = item[2]
         ssr['date'] = item[3]
         ssr['tn'] = item[4]
         ssr['idx'] = item[5]
         self.data['ssktkne'].append(ssr)