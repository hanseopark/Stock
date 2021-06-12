import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs

from tqdm import tqdm
import datetime

td_1y = datetime.timedelta(weeks=52/2)
start_day = datetime.datetime(2010,1,1)
today = datetime.datetime.now()
#start_day = today-td_1y

etf_list = yfs.tickers_dow()
s= input("Choice of stock's list (dow, sp500, nasdaq, other): ")
if s == 'dow':
    etf_list = yfs.tickers_dow()
    filename = 'dow'
elif s == 'sp500':
    filename = 'sp500'
    etf_list = yfs.tickers_sp500()
elif s == 'nasdaq':
    filename = 'nasdaq'
    etf_list = yfs.tickers_nasdaq()
elif s == 'other':
    filename = 'other'
    etf_list = yfs.tickers_other()
elif s == 'selected':
    filename = 'selected'
    url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
    temp_pd = pd.read_json(url)
    temp_pd = temp_pd['Ticker']
    etf_list = temp_pd.values.tolist()

print(etf_list)

etf_values = {}

error_symbols = []
for ticker in tqdm(etf_list):
    try:
        df = pdr.DataReader(ticker,'yahoo', start_day, today)
        etf_values[ticker] = df
    except:
        error_symbols.append(ticker)

combined_value = pd.concat(etf_values)
combined_value = combined_value.reset_index()
combined_value= combined_value.rename(columns={'level_0': 'Ticker'})

print(combined_value)

url = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_Value.json'.format(filename)
combined_value.to_json(url)
