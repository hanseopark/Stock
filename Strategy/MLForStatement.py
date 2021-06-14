import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

import json

## Get list of Dow tickers
dow_list = yfs.tickers_dow()
filename = ''
s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
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
elif s == 'selected':
    filename = 'selected'
    url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
    temp_pd = pd.read_json(url)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()
print(dow_list)
with open('../data_origin/{}.json'.format(filename),'w') as f:
    json.dump(dow_list, f)

## Read data
url = '/Users/hanseopark/Work/stock/'
url_price = url+'/data_origin/FS_{0}_Value.json'.format(filename)
url_stats = url+'/data_origin/FS_{0}_stats.json'.format(filename)
url_addstats = url+'/data_origin/FS_{0}_addstats.json'.format(filename)
url_balsheets = url+'/data_origin/FS_{0}_balsheets.json'.format(filename)
url_income = url+'/data_origin/FS_{0}_income.json'.format(filename)
url_flow = url+'/data_origin/FS_{0}_flow.json'.format(filename)

combined_price = pd.read_json(url_price)
combined_stats = pd.read_json(url_stats)
combined_addstats = pd.read_json(url_addstats)
combined_balsheets = pd.read_json(url_balsheets)
combined_income = pd.read_json(url_income)
combined_flow = pd.read_json(url_flow)

## Data preprocesing
# get price for eact stock
df_price = pd.DataFrame({'Recent_price': []})
for symbol in tqdm(dow_list):
    temp_df = combined_price[combined_price.Ticker.str.contains(symbol)]
    res = temp_df.loc[temp_df.index[-1], 'Adj Close']
    df_price.loc[symbol, 'Recent_price'] = res
df_price.to_json(url+'/data_preprocessing/{0}_Recent_price.json'.format(filename))
df_price.to_csv(url+'/data_preprocessing/{0}_Recent_price.csv'.format(filename))

# get P/E ratio for each stock
df_per = combined_stats[combined_stats.Attribute.str.contains("Trailing P/E")]
df_per = df_per.reset_index()
df_per['PER'] = df_per['Recent'].astype(float)
df_per = df_per.drop(['index', 'Attribute', 'Recent'], axis = 1)
df_per = df_per.set_index('Ticker')
df_per.to_json(url+'/data_preprocessing/{0}_per.json'.format(filename))
df_per.to_csv(url+'/data_preprocessing/{0}_per.csv'.format(filename))

# get P/S ratio for each stock
df_psr = combined_stats[combined_stats.Attribute.str.contains('Price/Sales')]
df_psr = df_psr.reset_index()
df_psr['PSR'] = df_psr['Recent'].astype(float)
df_psr = df_psr.drop(['index', 'Attribute', 'Recent'], axis = 1)
df_psr = df_psr.set_index('Ticker')
df_psr.to_json(url+'/data_preprocessing/{0}_psr.json'.format(filename))
df_psr.to_csv(url+'/data_preprocessing/{0}_psr.csv'.format(filename))

# get Price-to-Book ratio for each stock
df_pbr = combined_stats[combined_stats.Attribute.str.contains("Price/Book")]
df_pbr = df_pbr.reset_index()
df_pbr['PBR'] = df_pbr['Recent'].astype(float)
df_pbr = df_pbr.drop(['index', 'Attribute', 'Recent'], axis = 1)
df_pbr = df_pbr.set_index('Ticker')
df_pbr.to_json(url+'/data_preprocessing/{0}_pbr.json'.format(filename))
df_pbr.to_csv(url+'/data_preprocessing/{0}_pbr.csv'.format(filename))

# get PEG ratio for each stock
df_pegr = combined_stats[combined_stats.Attribute.str.contains('PEG')]
df_pegr = df_pegr.reset_index()
df_pegr['PEG ratio'] = df_pegr['Recent'].astype(float)
df_pegr = df_pegr.drop(['index', 'Attribute', 'Recent'], axis = 1)
df_pegr = df_pegr.set_index('Ticker')
df_pegr.to_json(url+'/data_preprocessing/{0}_pegr.json'.format(filename))
df_pegr.to_csv(url+'/data_preprocessing/{0}_pegr.csv'.format(filename))

# get foward P/E ratio for each stock
df_fowper = combined_stats[combined_stats.Attribute.str.contains('Forward P/E')]
df_fowper = df_fowper.reset_index()
df_fowper['Forward PER'] = df_fowper['Recent']
df_fowper = df_fowper.drop(['index', 'Attribute', 'Recent'], axis = 1)
df_fowper = df_fowper.set_index('Ticker')
df_fowper.to_json(url+'/data_preprocessing/{0}_forper.json'.format(filename))
df_fowper.to_csv(url+'/data_preprocessing/{0}_forper.csv'.format(filename))

# see additional stats
# get ROE for each stock
df_roe = combined_addstats[combined_addstats.Attribute.str.contains('Return on Equity')]
df_roe = df_roe.reset_index()
df_roe['ROE'] = df_roe['Value']
df_roe = df_roe.drop(['index', 'Attribute', 'Value'], axis = 1)
df_roe = df_roe.set_index('Ticker')
df_roe.to_json(url+'/data_preprocessing/{0}_roe.json'.format(filename))
df_roe.to_csv(url+'/data_preprocessing/{0}_roe.csv'.format(filename))

# get ROA for each stock
df_roa = combined_addstats[combined_addstats.Attribute.str.contains('Return on Assets')]
df_roa = df_roa.reset_index()
df_roa['ROA'] = df_roa['Value']
df_roa = df_roa.drop(['index', 'Attribute', 'Value'], axis = 1)
df_roa = df_roa.set_index('Ticker')
df_roa.to_json(url+'/data_preprocessing/{0}_roa.json'.format(filename))
df_roa.to_csv(url+'/data_preprocessing/{0}_roa.csv'.format(filename))

# get profit margin for each stock
df_pm = combined_addstats[combined_addstats.Attribute.str.contains('Profit Margin')]
df_pm = df_pm.reset_index()
df_pm['Profit Margin'] = df_pm['Value']
df_pm = df_pm.drop(['index', 'Attribute', 'Value'], axis = 1)
df_pm = df_pm.set_index('Ticker')
df_pm.to_json(url+'/data_preprocessing/{0}_pm.json'.format(filename))
df_pm.to_csv(url+'/data_preprocessing/{0}_pm.csv'.format(filename))


# see balance sheets
# get total assets
df_ta = combined_balsheets[combined_balsheets.Breakdown == 'totalAssets']
df_ta = df_ta.reset_index()
df_ta['Total assets'] = df_ta['Recent']
df_ta = df_ta.drop(['index', 'Breakdown', 'Recent'], axis = 1)
df_ta = df_ta.set_index('Ticker')
df_ta.to_json(url+'/data_preprocessing/{0}_ta.json'.format(filename))
df_ta.to_csv(url+'/data_preprocessing/{0}_ta.csv'.format(filename))

# See income statement
# get total revenue
df_tr = combined_income[combined_income.Breakdown == 'totalRevenue']
df_tr = df_tr.reset_index()
df_tr['Total revenue'] = df_tr['Recent']
df_tr = df_tr.drop(['index', 'Breakdown', 'Recent'], axis = 1)
df_tr = df_tr.set_index('Ticker')
df_tr.to_json(url+'/data_preprocessing/{0}_tr.json'.format(filename))
df_tr.to_csv(url+'/data_preprocessing/{0}_tr.csv'.format(filename))


# see cash flow
# get dividends paid across companies
df_div = combined_flow[combined_flow.Breakdown == 'dividendsPaid']
df_div = df_div.reset_index()
df_div['Dividends'] = df_div['Recent']
df_div = df_div.drop(['index', 'Breakdown', 'Recent'], axis = 1)
df_div = df_div.set_index('Ticker')
df_div.to_json(url+'/data_preprocessing/{0}_div.json'.format(filename))
df_div.to_csv(url+'/data_preprocessing/{0}_div.csv'.format(filename))

# get stock issuance information
df_iss = combined_flow[combined_flow.Breakdown == 'issuanceOfStock']
df_iss = df_iss.reset_index()
df_iss['Isuuance'] = df_iss['Recent']
df_iss = df_iss.drop(['index', 'Breakdown', 'Recent'], axis = 1)
df_iss = df_iss.set_index('Ticker')
df_iss.to_json(url+'/data_preprocessing/{0}_iss.json'.format(filename))
df_iss.to_csv(url+'/data_preprocessing/{0}_iss.csv'.format(filename))

# Merge dataframe
df = pd.concat([df_per, df_psr, df_pbr, df_pegr, df_fowper, df_roe, df_roa, df_pm, df_ta, df_tr, df_div, df_iss, df_price], axis =1)
print(df)

# Split data and test
train_df, test_df = train_test_split(df, test_size=0.2)

## Correlation for features
corrmat = train_df.corr()
top_corr_features = corrmat.index[abs(corrmat['Recent_price'])>0]

# Heatmap
plt.figure(figsize=(13,10))
plt_corr = sns.heatmap(train_df[top_corr_features].corr(), annot=True)
plt.show()









