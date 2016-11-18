from yahoo_finance import Share
import datetime
 
def getStock(id):
  stock = Share(str(id)+'.TW')
  today = datetime.date.today() #todays date
  data = stock.get_price()
  return data
 
print getStock(2330)