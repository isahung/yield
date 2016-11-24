import datetime
import time
import stockid #stockid.py
import parse_stock #parse_stock.py

def main():
  print('Start time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
  stockid.deleteContent('yield.txt')
  stockid.gen_stockid()
  f = open('stockid.txt', 'r')        
  result = list()

  y = open('yield.txt','a')
  y.write(" ID   Price  Avg. SD\n")

  for line in f.readlines():      
    line = line.strip()
    y = open('yield.txt','a')
    # check the yield rate is > 6.25%
    stock_yield = parse_stock.get_yield(line)
    stock_price = parse_stock.get_price()
    time.sleep(2)
    if(stock_price == None):
      continue
    if stock_yield/float(stock_price) >= 0.0625:
      y.write(line + str('  ') + stock_price + str('   ') + str(stock_yield) + str('\n'))
  print('Finish time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

if __name__ == "__main__":
  main()