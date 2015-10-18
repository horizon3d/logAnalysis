logs = []
detr = '---------------------------User: chengchen   SID: 55---------------------------\r\n2015 September 22, Tuesday, 16:54:57\r\n>detr tn  9999686012042 \r\n DETR:TN  9999686012042                                                        \r\nISSUED BY: AIR CHINA                 ORG/DST: BJS/SHA                 BSP-I     \r\nE/R: 9BJ10G0C/NONEND                                                            \r\nTOUR CODE: X9BJ10G0C                                         RECEIPT PRINTED  \r\nPASSENGER: DONG/XUEMIN                                                          \r\nEXCH:                               CONJ TKT:                                   \r\nO FM:1PEK CA     995  Z 08SEP 1500 OK ZXAP7H/NA  08SEP5/08SEP5 2PC USED/FLOWN   \r\n     T3-- RL:NB416S  /HS3N8R1E BG:2/43K BN:149                                  \r\nO TO:2IAH CA     996  Z 25SEP 0100 OK ZWAP7H/NA  25SEP5/25SEP5 2PC OPEN FOR USE \r\n     --T3 RL:NB416S  /HS3N8R1E                                                  \r\nX TO:3PEK CA    1831  F 26SEP 0730 OK F/NA       26SEP5/26SEP5 2PC OPEN FOR USE \r\n     T3T2 RL:NB416S  /HS3N8R1E                                                 +'
rt = '2015 September 22, Tuesday, 16:55:11\r\n>RT NB416S\r\n  **ELECTRONIC TICKET PNR**                                                     \r\n 1.DONG/XUEMIN 2.JIE/LINPING NB416S                                             \r\n 3.  CA996  Z1  FR25SEP  IAHPEK RR2   0100 0450+1    E --T3                     \r\n 4.  CA1831 F1  SA26SEP  PEKSHA RR2   0730 0940      E T3T2                     \r\n 5.T BJS/PEK/T 010-85227818/CHINA INTERNATIONAL TRAVEL SERVICE                  \r\n 6.T BJS//YE CHANGJIANG                                                         \r\n 7.SSR TKNE CA HK1 PEKIAH 995 Z08SEP 9999686012042/1/P1                         \r\n 8.SSR TKNE CA HK1 PEKIAH 995 Z08SEP 9999686012043/1/P2                         \r\n 9.SSR TKNE CA HK1 IAHPEK 996 Z25SEP 9999686012043/2/P2                         \r\n10.SSR TKNE CA HK1 PEKSHA 1831 F26SEP 9999686012043/3/P2                        \r\n11.SSR TKNE CA HK1 IAHPEK 996 Z25SEP 9999686012042/2/P1                         \r\n12.SSR TKNE CA HK1 PEKSHA 1831 F26SEP 9999686012042/3/P1                       +'
tsu = "2015 September 22, Tuesday, 16:55:18\r\n>TSU 2/OPEN\r\nACCEPTED"
logs.append(detr)
logs.append(rt)
logs.append(tsu)

text = '---------------------------User: chengchen   SID: 55---------------------------\r\n2015 September 22, Tuesday, 16:39:57\r\n>da\r\nA*      22150   19SEP   1622    9   PEK099                                      \r\nB       AVAIL                                                                   \r\nC       AVAIL                                                                   \r\nD       AVAIL                                                                   \r\nE       AVAIL                                                                   \r\nPID   = 15792   HARDCOPY  = 1112                                                \r\nTIME =  1641    DATE =  19SEP     HOST = CAAC                                   \r\nAIRLINE = CA    SYSTEM =  TST_D1  APPLICATION =  1        \r\n\r\n\r\n\r\n2015 September 22, Tuesday, 16:43:23\r\n>detr tn 9992379354359\r\n DETR:TN 9992379354359                                                         \r\nISSUED BY: AIR CHINA                 ORG/DST: PEK/SHA                 ARL-D     \r\nE/R: 改期退票收费                                                               \r\nTOUR CODE:                                                                      \r\nPASSENGER: 黄静静                                                               \r\nEXCH:                               CONJ TKT:                                   \r\nO FM:1PEK CA    1831  P 18SEP 0730 OK F          18SEP5/18SEP5 40K USED/FLOWN   \r\n     T3T2 RL:                  BN:159                  INVOL ENDO               \r\n  TO: SHA                                                                       \r\nFC:M 18SEP15PEK CA SHA3840.00CNY3840.00END                                    \r\nFARE:           CNY 3840.00|FOP:CC/ H1                                          \r\nTAX:            CNY 50.00CN|OI:                                                +\r\n                                                                                \r\n\r\n2015 September 22, Tuesday, 16:43:27\r\n>tsu 1/open\r\nACCEPTED                 \r\n\r\n\r\n2015 September 22, Tuesday, 16:47:30\r\n>DA\r\nA*      22150   19SEP   1622    9   PEK112                                      \r\nB       AVAIL                                                                   \r\nC       AVAIL                                                                   \r\nD       AVAIL                                                                   \r\nE       AVAIL                                                                   \r\nPID   = 15792   HARDCOPY  = 1112                                                \r\nTIME =  1649    DATE =  19SEP     HOST = CAAC                                   \r\nAIRLINE = CA    SYSTEM =  TST_D1  APPLICATION =  1    \r\n\r\n2015 September 22, Tuesday, 16:47:30\r\n>DA\r\nA*      22150   19SEP   1622    9   PEK112                                      \r\nB       AVAIL                                                                   \r\nC       AVAIL                                                                   \r\nD       AVAIL                                                                   \r\nE       AVAIL                                                                   \r\nPID   = 15792   HARDCOPY  = 1112                                                \r\nTIME =  1649    DATE =  19SEP     HOST = CAAC                                   \r\nAIRLINE = CA    SYSTEM =  TST_D1  APPLICATION =  1                             '

def __debug(fmt, *args):
    detail = fmt % (args)
    print(detail)

import re

if __name__ == '__main__':
    pattern = re.compile(r'>tsu (\d{1})([/\S]*/open)', re.I)
    match = pattern.search(tsu)
    
    if match:
        tid = match.group(1)
        __debug('ticket id is: %s', tid)
        add = match.group(2)
        __debug('state is: %s', add)
    # usr, sid
    pattern = re.compile(r'[-]+User: ([\w]+)[ ]+SID: (\d+)[-]+', re.I)
    match = pattern.search(detr)
    if match:
        user = match.group(1)
        __debug('user: %s', user)
        sid = int(match.group(2))
        __debug('sid: %d', sid)
        
    # timestamp
    pattern = re.compile(r'(20\d{2}) ([a-zA-Z]+) (\d+), ([a-zA-Z]+), (\d+):(\d+):(\d+)', re.I)
    match = pattern.search(detr)
    if match:
        __debug('timestamp: %s', match.group())
        
    # command
    pattern = re.compile(r'>[, /:]*([\w]+)[:/ ,]', re.I)
    match = pattern.search(rt)
    if match:
        cmd = match.group(1)
        __debug('command: %s', cmd)
    
    # return
    pattern = re.compile(r'[\w /,:]+[\w][\s]*\n(.*)', re.I)
    match = pattern.search(detr)
    if match:
        cmd = match.group(1)
        __debug('return: %s', cmd)
        
    # tn
    pattern = re.compile(r'>[ ,:/]*detr tn[\s:,/]+([\d]+)', re.I)
    match = pattern.search(detr)
    if match:
        tn = match.group(1)
        __debug('tn: %s', tn)
        
    pattern = re.compile(r'PASSENGER: ([A-Za-z]+/[a-zA-Z]+)', re.I)
    match = pattern.search(detr)
    if match:
        passenger = match.group(1)
        __debug('passenger: %s', passenger)
      
    # get ticket info from detr
    pattern =  r':(\d{1})\w+ ([\w]+)[ ]+([\d]+)[ ]+([a-zA-Z]) (\d{2}[\w]{3} \d{4}) OK ([\s\w/-]+):(\w+)'
    tickets = re.findall(pattern, detr, re.I)
    if len(tickets):
        __debug("%d ticket included", len(tickets))
        alltickets = []
        for obj in tickets:
            ticket = {}
            ticket['idx'] = int(obj[0])
            ticket['comp'] = obj[1]
            ticket['plane'] = obj[2]
            ticket['magic'] = obj[3]

            pattern = re.compile(r'(\d{2})([A-Z]{3}) (\d{4})')
            match = pattern.search(obj[4])
            mon = match.group(2)
            day = match.group(1)
            time = match.group(3)
            ticket['state'] = obj[5]
            #ticket['pnr'] = obj[6]
            pattern = re.compile(r'RL:(\w+) ')
            match = pattern.search(obj[5])
            if match:
                ticket['pnr'] = match.group(1)
            ticket['date'] = '' + match.group(1) + match.group(2)
            __debug('ticket %d: %s', ticket['idx'], str(ticket))
            alltickets.append(ticket)
            
    # get ssr tkne from rt
    pattern = re.compile(r'SSR TKNE ([\w]+) [\w\d]+ [\w\d]+ (\d+) ([A-Z])(\d{2}\w{3}) (\d+)/(\d)/', re.I)
    takens = pattern.findall(rt)
    if len(takens):
        __debug("%d takens included", len(takens))
        seats = []
    
        idx = 0
        for item in takens:
            ssr = {}
            ssr['comp'] = item[0]
            ssr['plane'] = item[1]
            ssr['magic'] = item[2]
            ssr['date'] = item[3]
            ssr['tn'] = item[4]
            ssr['idx'] = item[5]
            __debug('idx: %d, ssr tkne: %s', idx, str(ssr))
            seats.append(ssr)
            idx += 1
            
    print('ok')