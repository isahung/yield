import datetime
import time
from progressive.bar import Bar
import stockid #stockid.py
import parse_stock #parse_stock.py

def id_count(filename):
  lines = 0
  for line in open(filename):
      lines += 1
  return lines

def main():
  print('Start time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
  stockid.deleteContent('yield.txt')
  stockid.gen_stockid()
  f = open('stockid.txt', 'r')        
  result = list()

  line_count = id_count('stockid.txt')

  y = open('yield.txt','a')
  y.write(" ID   Price  Avg. SD\n")

  count = 0

  bar = Bar(max_value=line_count, fallback=True)
  bar.cursor.clear_lines(2)
  bar.cursor.save()

  for line in f.readlines():      
    line = line.strip()
    y = open('yield.txt','a')
    # check the yield rate is > 6.25%
    stock_yield = parse_stock.get_yield(line)
    stock_price = parse_stock.get_price()
    historical_price = parse_stock.historical_price(int(line))
    time.sleep(3)
    if(stock_price == None):
      continue
    if (stock_yield/float(stock_price) >= 0.0625 and float(stock_price)/historical_price <= 0.6 and float(stock_price) >= 20):
      y.write(line + str('  ') + stock_price + str('   ') + str(stock_yield) + str('\n'))
    count = count + 1
    bar.cursor.restore()
    bar.draw(value=count)
  print('Finish time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

if __name__ == "__main__":
  main()