# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
 
def deleteContent(fName):
  with open(fName, "w"):
    pass

def historical_price(index):
  url = "http://www.twse.com.tw/ch/trading/exchange/FMNPTK/genpage/Report201612/%d_F3_1_11.php?STK_NO=%d&myear=2016&mmon=12"%(index,index)
  res = requests.get(url, verify=False)
  soup = BeautifulSoup(res.text,'html.parser')
     
  for row in soup.select('tr'):
    cols = row.find_all('td')
    col1 = cols[0].text.encode('utf-8')
    data = re.search(r'(.*)    　(.*)',col1)
    print data
    if data is not None:
      if data.group(1) is not None:
        if data.group(2) is not None:
          if (len(cols[4].text.encode('utf-8')) != 0):
            symbolid =  filter(str.isalnum,data.group(1))
            #symbol = data.group(2)
            #start = cols[2].text.encode('utf-8')
            #type = cols[4].text.encode('utf-8')
            #print symbolid,symbol,start,type
            #f = open('stockid.txt','a')
            #f.write(symbolid+'\n')

def gen_stockid():
  deleteContent('stockid.txt')
  parse_stockid(2)
  parse_stockid(4)


def main():
  historical_price(2330)

if __name__ == "__main__":
  main()
