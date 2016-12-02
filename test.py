# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

def historical_price(index):
  DATA = {'STK_NO':str(index)}
  url = "http://www.twse.com.tw/ch/trading/exchange/FMNPTK/FMNPTK.php"
  res = requests.post(url, DATA)

  url = "http://www.twse.com.tw/ch/trading/exchange/FMNPTK/genpage/Report201612/%d_F3_1_11.php?STK_NO=%d&myear=2016&mmon=12"%(index,index)
  res = requests.get(url, verify=False)
  soup = BeautifulSoup(res.text,'html.parser')
  
  row = soup.find_all('tr', attrs={ 'bgcolor' : "#FFFFFF" })
  count = len(row)
  if (count == 0):
    return 0
  # TWSE
  else:
    col1 = row[count-3].find_all('td')
    col2 = row[count-2].find_all('td')
    ncol1 = float(col1[4].text)
    ncol2 = float(col2[4].text)
    if (ncol1 >= ncol2):
      #print ncol1
      return ncol1
    else:
      #print ncol2
      return ncol2

def main():
  print historical_price(2324)

if __name__ == "__main__":
  main()