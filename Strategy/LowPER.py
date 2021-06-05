import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

from classStrategy import FinancialStatements

# For NASDAQ
df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()


# For S&P500
pers_10 = pd.DataFrame({'PER': ['']}, index=['AAPL'])
pers_20 = pd.DataFrame({'PER': ['']}, index=['AAPL'])

url_sp500 = '../data/FS.json'
df_sp500 = pd.read_json(url_sp500)

error_symbols = []
for s in df_sp500.index.values:
    per = df_sp500.loc[s, 'PER']
    try:
        per = float(per)
        if (per < 20.0):
            pers_20.loc[s,'PER'] = per
            if (per < 10.0):
                pers_10.loc[s,'PER'] = per


    except:
        error_symbols.append(s)


print(pers_10)
print(pers_20)

url_10 = '../data/tableLowPER_10.json'
url_20 = '../data/tableLowPER_20.json'
pers_10.to_json(url_10)
pers_20.to_json(url_20)
