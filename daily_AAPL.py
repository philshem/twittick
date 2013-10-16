#!/usr/bin/env python
#
# Copyright 2013 Philip Shemella
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#'''A library that provides a Python interface to the Twitter API'''

#__author__ = 'psny18@gmail.com'
#__version__ = '0.1.0'

# this code takes a stock quote from markitondemand's API and posts it to twitter
# the following code is designed for Apple stock (AAPL).
 
import oauth2 as oauth
import requests
import urllib2
import simplejson as json
from requests_oauthlib import OAuth1

import twitter # https://github.com/bear/python-twitter

def markit():
#    quote = urllib2.urlopen('http://dev.markitondemand.com/Api/Quote/jsonp?symbol=AAPL&callback=myFunction')
    quote = urllib2.urlopen('http://dev.markitondemand.com/Api/Quote/json?symbol=AAPL')
    quote = json.load(quote)

# JSON output has this structure
#
# {'Data': {'Status': 'SUCCESS', 'High': 492.85, 'Name': 'Apple Inc', 'LastPrice': 487.115, 'Timestamp': 'Fri Aug 30 15:59:59 UTC-04:00 2013', 'Symbol': 'AAPL', 'ChangePercent': -0.0207300252865306, 'Volume': 568074, 'ChangePercentYTD': -8.466778372217, 'Low': 486.51, 'ChangeYTD': 532.1729, 'MarketCap': 442542516155, 'Open': 492.01, 'Change': -0.100999999999999}}

    printlist = []
    old_time = ''
    tag = ''
#    if True:
    if quote['Data']['Status'] == 'SUCCESS':
        symbol = quote['Data']['Symbol']
        high = quote['Data']['High']
        name = quote['Data']['Name']
        lastprice = quote['Data']['LastPrice']
        timestamp = quote['Data']['Timestamp']
        changepercent = quote['Data']['ChangePercent']
        volume = quote['Data']['Volume']
        changepercentytd = quote['Data']['ChangePercentYTD']
        low = quote['Data']['Low']
        changeytd = quote['Data']['ChangeYTD']
        marketcap = quote['Data']['MarketCap']
        opened = quote['Data']['Open']
        change = quote['Data']['Change']

# get direction
        if change > 0.0:
            direction = 'up'
        elif change < 0.0:
            direction = 'down'
        else:
            direction = 'flat'

# make printlist
        printlist.append('#Apple stock update - ')
        printlist.append(''.join(('$',str(symbol))))
        printlist.append(': $')
        printlist.append(str('{0:.2f}'.format(lastprice)))
        printlist.append(', ')
        printlist.append(direction)
        printlist.append(' ')
        printlist.append(str('{0:.2f}'.format(change)))
        printlist.append(' (')
        printlist.append(str('{0:.2f}'.format(changepercent)))
        printlist.append('%)')
        dt = timestamp.split()
#        if int(dt[3]) == 9
        newtime = ' on '+dt[0]+' '+dt[1]+' '+dt[2]+ \
            ' '+dt[5]+' at '+dt[3]+' EST'
        printlist.append(newtime)

        tt=dt[3].split(':')
        if tag != ' (close) ' and int(tt[0]) == 15 and int(tt[1]) == 59:
            tag = ' (close) '
            printlist.append(tag)
        elif int(tt[0]) == 9 and int(tt[1]) == 30:
            tag = ' (open) '
            printlist.append(tag)

    if timestamp != old_time:
        status = ''.join(''.join(key) for key in printlist)
    else:
        status = ''

    old_time = timestamp
#    print status
    return status
        
def twit(status):
    api = twitter.Api(consumer_key='consumer_key', \
                          consumer_secret='consumer_secret', \
                          access_token_key='access_token_key', \
                          access_token_secret='access_token_secret')

    status = api.PostUpdate(status)
    print status.text

if __name__ == "__main__":
    status = ''
    status = markit()
#    print status
    if status != '':
#        print status
        twit(status)
