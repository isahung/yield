from yahoo_finance import Share
import datetime
import stockid
import time
 
def getStock(id):
  stock = Share(str(id)+'.TW')
  today = datetime.date.today() #todays date
  data = stock.get_price()
  #time.sleep(0.1)
  return data
 
print('Start time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
stockid.deleteContent('yield.txt')
stockid.gen_stockid()
f = open('stockid.txt', 'r')        
result = list()
for line in f.readlines():      
  line = line.strip()
  y = open('yield.txt','a')
  y.write(line + str('  ') + getStock(line) + str('\n'))
print('Finish time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))