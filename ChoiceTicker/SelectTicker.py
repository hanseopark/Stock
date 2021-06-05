import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

from classFinancialStatements import FinancialStatements

# For NASDAQ
df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()


# For S&P500
url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
df_sp500 = pd.read_csv(url)

#print(df_sp500)
#print(yfs.get_quote_table('aapl'))


df = pd.DataFrame({'PER':[''], 'PBR':[''], 'Sector':[''], 'Beta':['']})
pers_10 = pd.DataFrame({'PER': ['']})
pers_20 = pd.DataFrame({'PER': ['']})
url_sp500 = '../data/FS.json'
#df = pd.read_json(url_sp500)
#print(df)

error_symbols = []
for s in df_sp500["Symbol"]:
    #if(s!= df.index.values):
    try:
        FS = FinancialStatements(s)
        per = FS.get_PER()
        pbr = FS.get_PBR()
        sector = FS.get_SECTOR()
        beta = FS.get_Beta()
        df.loc[s, 'PER'] = per
        df.loc[s, 'PBR'] = pbr
        df.loc[s, 'Sector'] = sector
        df.loc[s, 'Beta'] = beta
        print(s)
        df.to_json(url_sp500)
    except:
        print('error:', s)
        error_symbols.append(s)

# Save

