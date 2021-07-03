# I haven't yet understood thing.
# It is testing

from tqdm import tqdm

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

#from datetime import datetime, timedelta
#d = datetime(2020,1,1)
#now = datetime.now()
#print(d.isoformat())
#print(d.strftime("%Y-%m-%d"))
#print(d.strftime("%Y"))
#print(d.strftime("%m"))
#print(now.strftime("%m"))
#print(int(now.strftime("%m")))
#print(now.strftime("%d"))
#print(int(now.strftime("%d")))

#from Strategy.class_Strategy import LongTermStrategy
#import yahoo_fin.stock_info as yfs
#url = '/Users/hanseopark/Work/stock/' # in data
#filename='nasdaq'
#strategy = LongTermStrategy(url, filename, Offline= False) # Select Long term strategy
#df =strategy.get_CAP()
#print(df)
#df = strategy.get_Cash()
#df = strategy.get_Debt()
#df = strategy.get_addstats(True)

#dow_list = yfs.tickers_sp500()
#dow_list = yfs.tickers_nasdaq()

#print(df)
#df = strategy.get_balsheets_element(dow_list)
#df = strategy.get_income_element(dow_list)
#df = strategy.get_income_element()
#df = strategy.get_flow_element()
#df = strategy.get_flow_element(dow_list)
#print(df.info)
#print(df.dtypes)
#df_stats = strategy.get_stats(True)
#df_psr = strategy.get_PSR()

import yahoo_fin.stock_info as yfs
import pandas as pd
from tqdm import tqdm

#dow_list = yfs.tickers_sp500()
dow_list = ['SOFI']
dow_balsheets = {}

for ticker in tqdm(dow_list):
    sheets = yfs.get_balance_sheet(ticker)
    dow_balsheets[ticker] = sheets

print(dow_balsheets)


recent_sheets = {ticker : sheet.iloc[:,:4] for ticker, sheet in dow_balsheets.items()}
for ticker in recent_sheets.keys():
    recent_sheets[ticker].columns = ["Recent", "Before1", "Before2", "Before3"]

combined_balsheets = pd.concat(recent_sheets)
combined_balsheets = combined_balsheets.reset_index()

combined_balsheets.columns = ['Ticker', 'Breakdown', 'Recent', 'Before1', "Before2", "Before3"]


print(combined_balsheets)

combined_balsheets.to_csv('test.csv')
















