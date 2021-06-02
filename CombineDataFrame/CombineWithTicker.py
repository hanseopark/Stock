import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

#from classPER import FinancialStatements

# For NASDAQ
#df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()


# For S&P500

url_sp500 = '../data/FS.json'
url_PER_10 = '../data/tableLowPER_10.json'
url_PER_20 = '../data/tableLowPER_20.json'
url_PBR = '../data/tableLowPBR.json'

df_sp500 = pd.read_json(url_sp500)
df_PER_10 = pd.read_json(url_PER_10)
df_PER_20 = pd.read_json(url_PER_20)
df_PBR = pd.read_json(url_PBR)

df_sp500 = df_sp500.dropna()
print(df_sp500)
df_PER_10_PBR = df_sp500.join(df_PER_10)
df = pd.merge(df_sp500,df_PER_10)
print(df)

#print(df_PER_10_PBR)


