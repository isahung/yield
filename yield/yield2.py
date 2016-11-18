#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import csv

def GetHtmlcode(ID):
  # Get the webpage's source html code
  source = 'http://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='
  url = source + ID

  # Header
  headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
              'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset' : 'Big5,utf-8;q=0.7,*;q=0.3',
              #'Accept-Encoding' : 'gzip,deflate,sdch',
              'Accept-Language' : 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' ,
              'Cache-Control' : 'max-age=0',
              'Connection' : 'keep-alive',
              'Cookie' : '427 bytes were stripped',
              'Host' : 'www.goodinfo.tw',
              'Referer' : url }

  req= urllib2.Request(url,"",headers)
  response = urllib2.urlopen(req)
  result = response.read().decode('utf-8')
  #print result
  return result

def parse_stock(page):
  regex = re.compile("\<title\>(.*)\<\/title\>")
  title = regex.findall(page)[0]
  title = title[:title.find('-')].strip()
  #print title

  regex = re.compile('<table[\s\S]*?<\/table>')
  #print page
  datatable = regex.findall(page)
  #print datatable
  #print len(datatable)

  data_dict = {}
  Dividends_list = []
  list_ = []

  for l in datatable:
    if l.find(u'\u8fd1&nbsp;10&nbsp;\u5e74&nbsp;\u80a1&nbsp;\u5229&nbsp;\u653f&nbsp;\u7b56') != -1:
      #print l
      split_html_tags(l, Dividends_list)

  Dividends_list = group_list(Dividends_list, 4)

  for i in Dividends_list:
    print i

  print '\n'
  
  data_dict['stockid'] = title
  data_dict['yield'] = Dividends_list

  #list_.append(Dividends_list)
  return data_dict

def split_html_tags(tables, list_):
  #print tables.encode('utf-8')
  #print tables
  regex = re.compile("<tr align='center'[\s\S]*?<\/tr>")
  datarow = regex.findall(tables)
  #print datarow
  #print len(datarow)
  datarow = datarow[1:]
  str_convert = ''.join(datarow)

  string = str_convert.strip()
  #print string

  regex = re.compile('<td[\S\s]*?>(\w+|[0-9]+\.[0-9]+]*|[0-9]+\,[0-9]*|\-[0-9]+\.[0-9]+]*|\-\d+|\-)<\/td>')
  data = regex.findall(string)

  #print data

  for i in data:
      list_.append(i)

def group_list(l,block):
  size = len(l)
  return [l[i:i+block] for i in range(0,size,block)]

def pasre_stock_value(dict_):

    print '\n'
    print dict_['stockid']
    print '\n'

    Dividends_list = []

    Dividends_list = dict_['yield']
    
    if len(Dividends_list) >= 5:
        Dividends_year = 5
    else:
        Dividends_year = len(Dividends_list)

    #print Dividends_list
    sum = 0.0
    # 5 years average yield rate
    for i in range(0, Dividends_year):
        #print float(Dividends_list[i][3])
        sum += float(Dividends_list[i][3])  

    #print sum / float(Dividends_year)
    return sum

def main():
  fin = open('stockid.txt', 'r+')
  StockCodeList = [str(i)for i in fin.read().splitlines()]
  fin.close()

  page = GetHtmlcode('2330')
  dict_ = parse_stock(page)

  pasre_stock_value(dict_)

if __name__ == "__main__":
  main()