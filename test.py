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

from Strategy.class_Strategy import LongTermStrategy
#import yahoo_fin.stock_info as yfs
url = '/Users/hanseopark/Work/stock/' # in data
filename='sp500'
strategy = LongTermStrategy(url, filename, Offline= False) # Select Long term strategy
#df =strategy.get_TA()
df_2 = strategy.get_balsheets_element()
#print(df)
print(df_2)
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

#import yahoo_fin.stock_info as yfs
#import pandas as pd
#from tqdm import tqdm
#
##dow_list = yfs.tickers_sp500()
#dow_list = ['AAPL', 'CRL', 'ODFL', 'PWR', 'UDR']
#dow_balsheets = {}
#
#error_symbol = []
#for ticker in tqdm(dow_list):
#	try:
#		sheets = yfs.get_balance_sheet(ticker)
#		dow_balsheets[ticker] = sheets
#	except:
#		error_symbol.append(ticker)
#
#print(dow_balsheets)
#print(error_symbol)
#
#
##recent_sheets = {ticker : sheet.iloc[:,:4] for ticker, sheet in dow_balsheets.items()}
##print(recent_sheets)
#for ticker in dow_balsheets.keys():
#	try:
#		dow_balsheets[ticker].columns = ["Recent", "Before1", "Before2", "Before3"]
#	except:
#		error_symbol.append(ticker)
#print(error_symbol)
##    except:
##        print(ticker)
#
#combined_balsheets = pd.concat(dow_balsheets)
#combined_balsheets = combined_balsheets.reset_index()
#
#combined_balsheets.columns = ['Ticker', 'Breakdown', 'Recent', 'Before1', "Before2", "Before3"]
#
#print(combined_balsheets)
#
#combined_balsheets.to_csv('test.csv')
















