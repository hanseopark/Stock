import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

from classStrategy import BasicStrategy

url = '/Users/hanseopark/Work/stock/data_ForTrading/output.json'
temp_pd = pd.read_json(url)
temp_pd = temp_pd['Ticker']
stock_list = temp_pd.values.tolist()

stats = {}
for ticker in stock_list:
    temp = yfs.get_stats_valuation(ticker)
    temp = temp.iloc[:,:2]
    temp.columns = ['Attribute', 'Recent']

    stats[ticker] = temp

combined_stats = pd.concat(stats)
combined_stats = combined_stats.reset_index()

del combined_stats['level_1']

combined_stats.columns = ['Ticker', 'Attribute', "Recent"]

# get P/E ratio for each stock
df = combined_stats[combined_stats.Attribute.str.contains('Trailing P/E')]

print(df)
