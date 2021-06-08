import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

from classStrategy import BasicStrategy

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

s2 = input("Choice of stock's statement (per, pbr): ")
if s2 == 'per':
    statement = 'stats'
    url = '../data/FS_{0}_{1}.json'.format(filename, statement)

df = pd.read_json(url)
df_per = df[df.Attribute.str.contains("Trailing P/E")]
print(df_per)

## For NASDAQ
#df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()
#
#
## For S&P500
#pers_10 = pd.DataFrame({'PER': ['']}, index=['AAPL'])
#pers_20 = pd.DataFrame({'PER': ['']}, index=['AAPL'])
#
#url_sp500 = '../data/FS.json'
#df_sp500 = pd.read_json(url_sp500)
#
#error_symbols = []
#for s in df_sp500.index.values:
#    per = df_sp500.loc[s, 'PER']
#    try:
#        per = float(per)
#        if (per < 20.0):
#            pers_20.loc[s,'PER'] = per
#            if (per < 10.0):
#                pers_10.loc[s,'PER'] = per
#
#
#    except:
#        error_symbols.append(s)
#
#
#print(pers_10)
#print(pers_20)
#
#url_10 = '../data/tableLowPER_10.json'
#url_20 = '../data/tableLowPER_20.json'
#pers_10.to_json(url_10)
#pers_20.to_json(url_20)
