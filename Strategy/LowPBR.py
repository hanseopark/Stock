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
df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()


# For S&P500
invest_pbr = pd.DataFrame({'PBR': ['']}, index=['Symbol'])

url_sp500 = '../data/FS.json'
df_sp500 = pd.read_json(url_sp500)
df_pbr = df_sp500['PBR']

error_symbols = []
for s in df_sp500.index.values:
    pbr = df_sp500.loc[s, 'PBR']
    try:
        pbr = float(pbr)
        if (pbr > 0.):
            df_pbr.loc[s, 'PBR'] = pbr
    except:
        error_symbols.append(s)

try:
    df_pbr = df_pbr.astype(str)
    df_pbr = df_pbr.sort_values()
except:
    pass

df_pbr = df_pbr.head(30)
#print(df_pbr)

url = '../data/tableLowPER.json'
df_pbr.to_json(url)

