import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import json
from classStrategy import BasicStrategy

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

## Read data
url_stats = '/Users/hanseopark/Work/stock/data/FS_{0}_stats.json'.format(filename)
url_addstats = '/Users/hanseopark/Work/stock/data/FS_{0}_addstats.json'.format(filename)
url_balsheets = '/Users/hanseopark/Work/stock/data/FS_{0}_balsheets.json'.format(filename)
url_income = '/Users/hanseopark/Work/stock/data/FS_{0}_income.json'.format(filename)
url_flow = '/Users/hanseopark/Work/stock/data/FS_{0}_flow.json'.format(filename)

combined_stats = pd.read_json(url_stats)
combined_addstats = pd.read_json(url_addstats)
combined_balsheets = pd.read_json(url_balsheets)
combined_income = pd.read_json(url_income)
combined_flow = pd.read_json(url_flow)

## Data preprocesing
# get P/E ratio for each stock
df_per = combined_stats[combined_stats.Attribute.str.contains("Trailing P/E")]
df_per = df_per.reset_index()
df_per['PER'] = df_per['Recent']
df_per = df_per.drop(['index', 'Attribute', 'Recent'], axis = 1)

# get P/S ratio for each stock
df_psr = combined_stats[combined_stats.Attribute.str.contains('Price/Sales')]
df_psr = df_psr.reset_index()
df_psr['PSR'] = df_psr['Recent']
df_psr = df_psr.drop(['index', 'Attribute', 'Recent'], axis = 1)

# get Price-to-Book ratio for each stock
df_pbr = combined_stats[combined_stats.Attribute.str.contains("Price/Book")]
df_pbr = df_pbr.reset_index()
df_pbr['PBR'] = df_pbr['Recent']
df_pbr = df_pbr.drop(['index', 'Attribute', 'Recent'], axis = 1)

# get PEG ratio for each stock
df_pegr = combined_stats[combined_stats.Attribute.str.contains('PEG')]
df_pegr = df_pegr.reset_index()
df_pegr['PEG ratio'] = df_pegr['Recent']
df_pegr = df_pegr.drop(['index', 'Attribute', 'Recent'], axis = 1)

# get foward P/E ratio for each stock
df_fowper = combined_stats[combined_stats.Attribute.str.contains('Forward P/E')]
df_fowper = df_fowper.reset_index()
df_fowper['Forward PER'] = df_fowper['Recent']
df_fowper = df_fowper.drop(['index', 'Attribute', 'Recent'], axis = 1)

# see additional stats
# get ROE for each stock
df_roe = combined_addstats[combined_addstats.Attribute.str.contains('Return on Equity')]
df_roe = df_roe.reset_index()
df_roe['ROE'] = df_roe['Value']
df_roe = df_roe.drop(['index', 'Attribute', 'Value'], axis = 1)

# get ROA for each stock
df_roa = combined_addstats[combined_addstats.Attribute.str.contains('Return on Assets')]
df_roa = df_roa.reset_index()
df_roa['ROA'] = df_roa['Value']
df_roa = df_roa.drop(['index', 'Attribute', 'Value'], axis = 1)

# get profit margin for each stock
df_pm = combined_addstats[combined_addstats.Attribute.str.contains('Profit Margin')]
df_pm = df_pm.reset_index()
df_pm['Profit Margin'] = df_pm['Value']
df_pm = df_pm.drop(['index', 'Attribute', 'Value'], axis = 1)


# see balance sheets
# get total assets
df_ta = combined_balsheets[combined_balsheets.Breakdown == 'totalAssets']
df_ta = df_ta.reset_index()
df_ta['Total assets'] = df_ta['Recent']
df_ta = df_ta.drop(['index', 'Breakdown', 'Recent'], axis = 1)

# See income statement
# get total revenue
df_tr = combined_income[combined_income.Breakdown == 'totalRevenue']
df_tr = df_tr.reset_index()
df_tr['Total revenue'] = df_tr['Recent']
df_tr = df_tr.drop(['index', 'Breakdown', 'Recent'], axis = 1)


# see cash flow
# get dividends paid across companies
df_div = combined_flow[combined_flow.Breakdown == 'dividendsPai']
df_div = df_div.reset_index()
df_div['Dividends'] = df_div['Recent']
df_div = df_div.drop(['index', 'Breakdown', 'Recent'], axis = 1)

# get stock issuance information
df_iss = combined_flow[combined_flow.Breakdown == 'isuuanceOfStock']
df_iss = df_iss.reset_index()
df_iss['Isuuance'] = df_iss['Recent']
df_iss = df_iss.drop(['index', 'Breakdown', 'Recent'], axis = 1)

# merge dataframe
df = pd.merge(df_per, df_psr, how='outer', on='Ticker')
df = pd.merge(df, df_pbr, how='outer', on='Ticker')
df = pd.merge(df, df_pegr, how='outer', on='Ticker')
df = pd.merge(df, df_fowper, how='outer', on='Ticker')
df = pd.merge(df, df_roe, how='outer', on='Ticker')
df = pd.merge(df, df_roa, how='outer', on='Ticker')
df = pd.merge(df, df_pm, how='outer', on='Ticker')
df = pd.merge(df, df_ta, how='outer', on='Ticker')
df = pd.merge(df, df_tr, how='outer', on='Ticker')
df = pd.merge(df, df_div, how='outer', on='Ticker')
df = pd.merge(df, df_iss, how='outer', on='Ticker')

print(df)

