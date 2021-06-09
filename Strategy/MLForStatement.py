import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

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



