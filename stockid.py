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
    data = re.search(r'(.*)    　(.*)',col1)
    if data is not None:
      if data.group(1) is not None:
        if data.group(2) is not None:
          if (len(cols[4].text.encode('utf-8')) != 0):
            symbolid =  filter(str.isalnum,data.group(1))
            symbol = data.group(2)
            start = cols[2].text.encode('utf-8')
            type = cols[4].text.encode('utf-8')
            #print symbolid,symbol,start,type
            f = open('stockid.txt','a')
            f.write(symbolid+'\n')

def gen_stockid():
  deleteContent('stockid.txt')
  parse_stockid(2)
  parse_stockid(4)

'''
def main():
  gen_stockid()

if __name__ == "__main__":
  main()
'''