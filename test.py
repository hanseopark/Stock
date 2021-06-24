# I haven't yet understood thing.
# It is testing

#from Strategy.PlotStrategy import main as splt
#fig = splt('AAPL',False,'BB')
#fig.show()

#from Strategy.runStrategy import main as splt
#from Strategy.runStrategy import main as srun
#import yahoo_fin.stock_info as yfs
#dow_list = yfs.tickers_dow()
##strategy = LongTermStrategy(symbol, start_day, now_day)
#df_pred = srun(stock_list='dow', stats='ML')
#print(df_pred)


#from yahoo_fin import news
#
#s = news.get_yf_rss('AAPL')
##print(s)
#for k, v in enumerate (s):
#    print(k,v)


#import yahoo_fin.stock_info as yfs
#
#price = yfs.get_live_price('AAPL')
#print(price)

from datetime import datetime, timedelta
d = datetime(2020,1,1)
now = datetime.now()
print(d.isoformat())
print(d.strftime("%Y-%m-%d"))
print(d.strftime("%Y"))
print(d.strftime("%m"))
print(now.strftime("%m"))
print(int(now.strftime("%m")))
print(now.strftime("%d"))
print(int(now.strftime("%d")))
