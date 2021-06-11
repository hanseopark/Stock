import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import json
import datetime
from class_Strategy import LongTermStrategy, TrendStrategy

# Get datetime for price of stock
#td_1y = datetime.timedelta(weeks=52/2)
td_1y = datetime.timedelta(weeks=52)
today = datetime.datetime.now()
start_day = today - td_1y

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

# Select strategy for situation
LimitValue = 0
stats = input('Choice statement (PER, PBR, Trend): ')
if (stats == 'PER' or stats == "PBR"):
    strategy = LongTermStrategy(url, filename, statement= 'stats') # Select Long term strategy
    s2 = input('Set {} point(10, 20, 30): '.format(stats))
    LimitValue = int(s2)
elif stats == 'Trend':
    symbol = input('Write ticker name like aapl: ')
    dow_list = [symbol]
    strategy = TrendStrategy(symbol, start_day, today, keywords=dow_list)

# Perform strategy and save
url_threshold = '/Users/hanseopark/Work/stock/data_origin/table{0}_{1}_{2}.json'.format(stats, filename,LimitValue)
if stats == 'PER':
    df_per = strategy.LowPER(threshold = LimitValue)
    print(df_per)
    df_per.to_json(url_threshold)

elif stats == 'PBR':
    df_pbr = strategy.LowPBR(threshold = LimitValue)
    print(df_pbr)
    df_pbr.to_json(url_threshold)

elif stats == 'Trend':
    df_tr = strategy.get_trend_data()
    df_price = strategy.get_price_data(nomalization = True)

    index = df_price.astype('str')
    fig = plt.figure(figsize=(10,10))
    ax_main = plt.subplot(1,1,1)

    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except indexerror:
            return ''

    # ax_main
#    ax_main.xaxis.set_major_locator(ticker.maxnlocator(10))
#    ax_main.xaxis.set_major_formatter(ticker.funcformatter(x_date))
    ax_main.set_title("Stock's value with google trend", fontsize=22 )
    #ax_main.plot(df_price['Adj Close'], label='ORLY')
    for tic in dow_list:
        ax_main.plot(df_tr[tic], label='Trend')
    ax_main.plot(df_price['Adj Close'], label="Stock's value")
    ax_main.legend(loc=2)

    plt.grid()
    plt.show()











