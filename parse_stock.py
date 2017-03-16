#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import csv
import requests
from bs4 import BeautifulSoup

def get_average_dividend(index):
  url = "https://tw.stock.yahoo.com/d/s/dividend_%d.html"%(index)
  request = urllib2.Request(url) 
  request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

  response = urllib2.urlopen(request)  
  html = response.read()

  soup = BeautifulSoup(html,'html.parser')
  table = soup.find_all('table', attrs={ 'cellspacing' : "1", 'cellpadding' : "3" })
  row = table[0].find_all('tr', attrs={ 'bgcolor' : "#FFFFFF" })
  dividends_year = len(row)
  if (dividends_year == 0):
    return 0 
  if (dividends_year >= 5):
    dividends_year = 5

  dividends = 0.0

  for i in range(0, dividends_year):
    col = row[i].find_all('td')
    dividends += float(col[5].text)
  return dividends/dividends_year

def get_current_volume(index):
  url = "https://tw.stock.yahoo.com/q/q?s=%d"%(index)
  request = urllib2.Request(url) 
  request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

  response = urllib2.urlopen(request)  
  html = response.read()

  soup = BeautifulSoup(html,'html.parser')
  table = soup.find_all('table', attrs={ 'width' : "750", 'border' : "2" })
  row = table[0].find_all('td')

  if(row[6].text == u"－"):
    return 0

  return row[6].text.replace(',','')

def get_current_price(index):
  url = "https://tw.stock.yahoo.com/q/q?s=%d"%(index)
  request = urllib2.Request(url) 
  request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

  response = urllib2.urlopen(request)  
  html = response.read()

  soup = BeautifulSoup(html,'html.parser')
  table = soup.find_all('table', attrs={ 'width' : "750", 'border' : "2" })
  row = table[0].find_all('b')

  if(row[0].text == u"－"):
    return 0

  return row[0].text

def get_recent_PER(index):
  #print index
  url = "https://tw.stock.yahoo.com/d/s/company_%d.html"%(index)
  request = urllib2.Request(url) 
  request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

  response = urllib2.urlopen(request)  
  html = response.read()

  soup = BeautifulSoup(html,'html.parser')
  row = soup.find_all('tr', attrs={ 'bgcolor' : "#FFFFFF" })
  col12 = row[12].find_all('td')
  str1 = col12[3].text.encode('latin1', 'ignore').decode('big5')
  str1.encode("utf-8")
  str1 = str1.replace(u"元", u"")

  col13 = row[13].find_all('td')
  str2 = col13[3].text.encode('latin1', 'ignore').decode('big5')
  str2.encode("utf-8")
  str2 = str2.replace(u"元", u"")

  col14 = row[14].find_all('td')
  str3 = col14[3].text.encode('latin1', 'ignore').decode('big5')
  str3.encode("utf-8")
  str3 = str3.replace(u"元", u"")

  col15 = row[15].find_all('td')
  str4 = col15[3].text.encode('latin1', 'ignore').decode('big5')
  str4.encode("utf-8")
  str4 = str4.replace(u"元", u"")

  if (str1 == "-"):
    str1 = 0
  if (str2 == "-"):
    str2 = 0
  if (str3 == "-"):
    str3 = 0
  if (str4 == "-"):
    str4 = 0

  return float(str1) + float(str2) + float(str3) + float(str4)

def historical_price(index):
  DATA = {'STK_NO':str(index)}
  url = "http://www.twse.com.tw/ch/trading/exchange/FMNPTK/FMNPTK.php"
  res = requests.post(url, DATA)

  url = "http://www.twse.com.tw/ch/trading/exchange/FMNPTK/genpage/Report201702/%d_F3_1_11.php?STK_NO=%d&myear=2017&mmon=02"%(index,index)
  res = requests.get(url, verify=False)

  soup = BeautifulSoup(res.text,'html.parser')
  
  row = soup.find_all('tr', attrs={ 'bgcolor' : "#FFFFFF" })
  count = len(row)
  # OTC
  if (count == 0):
    DATA = {'input_stock_code':str(index)}
    url = "http://www.tpex.org.tw/web/stock/statistics/monthly/st42.php"
    res = requests.post(url, DATA)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find_all('table', attrs={ 'class' : "page-table-board" })
    row = table[0].find_all('tr')
    col1 = ""
    col2 = ""
    if (len(row) > 2):
      col1 = row[2].find_all('td')
    if (len(row) > 3):
      col2 = row[3].find_all('td')
    ncol1 = 0.0
    ncol2 = 0.0
    if (len(col1) > 4):
      ncol1 = float(col1[4].text.replace(',',''))
    if (len(col2) > 4):
      ncol2 = float(col2[4].text.replace(',',''))
    if (ncol1 >= ncol2):
      #print ncol1
      return ncol1
    else:
      #print ncol2
      return ncol2
  # TWSE
  else:
    col1 = ""
    col2 = ""
    if(count >= 3):
      col1 = row[count-3].find_all('td')
    if(count >= 2):
      col2 = row[count-2].find_all('td')

    ncol1 = 0.0
    ncol2 = 0.0
    if (len(col1) > 4):
      ncol1 = float(col1[4].text.replace(',',''))
    if (len(col2) > 4):
      ncol2 = float(col2[4].text.replace(',',''))
    if (ncol1 >= ncol2):
      #print ncol1
      return ncol1
    else:
      #print ncol2
      return ncol2

def main():
  print get_current_price(2330)
  print get_average_dividend(2330)
  print get_recent_PER(8481)
  print get_current_volume(8481)
  print get_current_price(8481)

if __name__ == "__main__":
  main()
