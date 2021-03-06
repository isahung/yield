# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
 
def deleteContent(fName):
  with open(fName, "w"):
    pass

def parse_stockid(index):
  url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=%d"%(index)
  res = requests.get(url, verify=False)
  soup = BeautifulSoup(res.text,'html.parser')
     
  for row in soup.select('tr'):
    cols = row.find_all('td')
    col1 = cols[0].text.encode('utf-8')
    data = re.search(r'(.*)　(.*)',col1)
    if data is not None:
      if data.group(1) is not None:
        if data.group(2) is not None:
          #print data.group(1)
          if (len(cols[4].text.encode('utf-8')) != 0):
            symbolid =  filter(str.isalnum,data.group(1))
            # stock id 3662, 6560, 8477 no data in TWSE 
            #if (symbolid != '3662' and symbolid != '6560' and symbolid != '8477'):
            if (len(symbolid) == 4):
              f = open('stockid.txt','a')
              f.write(symbolid+'\n')

def gen_stockid():
  deleteContent('stockid.txt')
  parse_stockid(2)
  parse_stockid(4)

def main():
  gen_stockid()

if __name__ == "__main__":
  main()