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
pers_10 = pd.DataFrame({'PER': ['']}, index=['Symbol'])
pers_20 = pd.DataFrame({'PER': ['']}, index=['Symbol'])

url_sp500 = '../data/FS.json'
df_sp500 = pd.read_json(url_sp500)

error_symbols = []
for s in df_sp500.index.values:
    per = df_sp500.loc[s, 'PER']
    try:
        per = float(per)
        if (per < 20.0):
            pers_20.loc[s,'PER'] = per
            if (int(df_sp500.loc[s, 'PER']) <10):
                pers_10.loc[s,'PER'] = per


    except:
        error_symbols.append(s)


#print(pers_10)
#print(pers_20)

url = '../data/tableLowPER.json'
pers_10.to_json(url)
pers_20.to_json(url)
