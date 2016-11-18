from yahoo_finance import Share
import datetime
import stockid
 
def getStock(id):
  stock = Share(str(id)+'.TW')
  today = datetime.date.today() #todays date
  data = stock.get_price()
  return data
 
stockid.gen_stockid()
print getStock(2330)