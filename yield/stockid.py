# -*- coding: utf-8 -*-
import re
import urllib2,urllib
import os

# get stock id and name
def getStockNumberAndName(index):
  try:
    # set STK01..23.php?STK=01 ... 23 
    url = 'http://www.twse.com.tw/ch/trading/inc/STKCHOICE/STK%02d.php?STK=%02d'%(index,index)
    req = urllib2.Request(url)
    rawData = urllib2.urlopen(req)
    tmpData = rawData.read()
    # from regular expression for 4 number id, findall and return an array 
    tmp = re.findall(u"<span class='basic2'>(\d{4})&nbsp;(.*)</span>",tmpData)
    return tmp
          
  except Exception , e:
    print e

def getAllStockNumberAndName():
  try:
    result = []
    for index in range(1,24): # all catalogs
      tmpResult = getStockNumberAndName(index)
      if(tmpResult):
        result += tmpResult
    return result
  except Exception , e:
    print e

def deleteContent(fName):
  with open(fName, "w"):
    pass

deleteContent('stockid.txt')
stockNumAndName = getAllStockNumberAndName()
#print stockNumAndName
for oneSet in stockNumAndName:
    #print oneSet[0] + oneSet[1]

  f = open('stockid.txt','a')
  f.write(oneSet[0] + oneSet[1]+'\n')