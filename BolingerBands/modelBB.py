import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import csv
import json
import datetime
from tqdm import tqdm

from classBB import Stocks

def main(stock_list, day_init=datetime.datetime(2020,1,1), today=datetime.datetime.now()):

    # Get list of Dow tickers
    dow_list = yfs.tickers_dow()
    filename = ''
    if stock_list == 'dow':
        dow_list = yfs.tickers_dow()
        filename = 'dow'
    elif stock_list == 'sp500':
        filename = 'sp500'
        dow_list = yfs.tickers_sp500()
    elif stock_list == 'nasdaq':
        filename = 'nasdaq'
        dow_list = yfs.tickers_nasdaq()
    elif stock_list == 'other':
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
        df_day_ago = df.iloc[-2]
        df_recent = df.iloc[-1:]
        #print(df_day_ago)
        #print(df_recent)
        value_day_ago_ago = float(df_day_ago_ago['Adj Close'])
        value_day_ago = float(df_day_ago['Adj Close'])
        value_recent = float(df_recent['Adj Close'])
        upper_recent = float(df_recent['bol_upper'])
        down_recent = float(df_recent['bol_down'])
        std_recent = float(df_recent['Std'])

        if std_recent < mean and value_recent > value_day_ago and value_day_ago > value_day_ago_ago and value_recent < upper_recent:
            selected_ticker.append(ticker)

    url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList.json'.format(today.date())
    df = pd.DataFrame(selected_ticker, columns=['Ticker'])
    #df.columns = ['Ticker']
    df.to_json(url)

    print(df)
    return df

if __name__ == '__main__':
    s_list= input("Choice of stock's list (dow, sp500, nasdaq, other): ")
    td_1y = datetime.timedelta(weeks=52/2)
    #start_day = datetime.datetime(2019,1,1)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(stock_list = s_list,day_init = start_day)
else:
    pass
