import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import json
from class_Strategy import LongTermStrategy

# Get list of Dow tickers
dow_list = yfs.tickers_dow()
filename = ''
s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
if s == 'dow':
    dow_list = yfs.tickers_dow()
    filename = 'dow'
elif s == 'sp500':
    filename = 'sp500'
    dow_list = yfs.tickers_sp500()
elif s == 'nasdaq':
    filename = 'nasdaq'
    dow_list = yfs.tickers_nasdaq()
elif s == 'other':
    filename = 'other'
    dow_list = yfs.tickers_other()
elif s == 'selected':
    filename = 'selected'
    url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
    temp_pd = pd.read_json(url)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

print('*'*100)
print(dow_list)
print('*'*100)

url = '/Users/hanseopark/Work/stock/data_origin/' # in data
strategy = LongTermStrategy(url, filename, statement= 'stats') # Select Long term strategy

## PER ##
stats = input('Choice statement (PER, PBR): ')
s2 = input('Set {} point(10, 20, 30): '.format(stats))
LimitValue = int(s2)

url_threshold = '/Users/hanseopark/Work/stock/data_origin/table{0}_{1}_{2}.json'.format(stats, filename,LimitValue)
if stats == 'PER':
    df_per = strategy.LowPER(threshold = LimitValue)
    print(df_per)
    df_per.to_json(url_threshold)

elif stats == 'PBR':
    df_pbr = strategy.LowPBR(threshold = LimitValue)
    print(df_pbr)
    df_pbr.to_json(url_threshold)








