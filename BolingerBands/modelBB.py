import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import csv
import json
import datetime
from tqdm import tqdm

#from classStrategy import BasicStrategy
from finance_class import Stocks

td_1y = datetime.timedelta(weeks=52/2)
#start_day = datetime.datetime(2019,1,1)
#end_day = datetime.datetime(2021,5,1)
today = datetime.datetime.now()
start_day = today - td_1y

# Get list of Dow tickers
dow_list = yfs.tickers_dow()
filename = ''
s= input("Choice of stock's list (dow, sp500, nasdaq, other): ")
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
print(dow_list)

selected_ticker = []
for ticker in tqdm(dow_list):
    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except IndexError:
            return ''

    stock = Stocks(ticker, start_day, today)
    df = stock.with_moving_ave()
    index = df.index.astype('str')
    mean = df['Std'].mean()
    df_day_ago_ago = df.iloc[-3]
    df_day_ago = df.iloc[-4]
    df_recent = df.iloc[-1:]
    #print(df_day_ago)
    #print(df_recent)
    value_day_ago = float(df_day_ago['Adj Close'])
    value_recent = float(df_recent['Adj Close'])
    upper_recent = float(df_recent['bol_upper'])
    down_recent = float(df_recent['bol_down'])
    std_recent = float(df_recent['Std'])

    if std_recent < mean:
        if value_recent > value_day_ago:
            if value_recent < upper_recent:
                selected_ticker.append(ticker)

url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList.json'.format(today.date())
df = pd.DataFrame(selected_ticker)
df.columns = ['Ticker']
df.to_json(url)
