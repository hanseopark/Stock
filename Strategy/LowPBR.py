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
df_sp500 = pd.read_json(url_sp500)
df_pbr = pd.DataFrame({'PBR': ['']}, index=['AAPL'])

error_symbols = []
for s in df_sp500.index.values:
    pbr = df_sp500.loc[s, 'PBR']
    try:
        pbr = float(pbr)
        df_pbr.loc[s, 'PBR'] = pbr
    except:
        error_symbols.append(s)

df_pbr = df_pbr.sort_values(by='PBR')

invest_pbr = df_pbr.head(30)
print(invest_pbr)

url = '../data/tableLowPBR.json'
invest_pbr.to_json(url)

