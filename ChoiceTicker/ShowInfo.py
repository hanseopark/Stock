import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import json
from tqdm import tqdm

url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
temp_pd = pd.read_json(url)
temp_pd = temp_pd['Ticker']
stock_list = temp_pd.values.tolist()

dow_stats = {}
dow_addstats = {}
dow_balsheets = {}
dow_income = {}
dow_flow = {}

for ticker in tqdm(stock_list):
    try:
        # Getteing Summary
        basic = yfs.get_stats_valuation(ticker)
        basic =basic.iloc[:,:2]
        basic.columns = ['Attribute', 'Recent']
        dow_stats[ticker] = basic

        # Getting additioanl stats
        add = yfs.get_stats(ticker)
        add.columns = ['Attribute', 'Value']
        dow_addstats[ticker] = add

        # Getting balance sheets
        sheets = yfs.get_balance_sheet(ticker)
        dow_balsheets[ticker] = sheets

        # Getting income statements
        income = yfs.get_income_statement(ticker)
        dow_income[ticker] = income

        # Getting cash flow statements
        flow = yfs.get_cash_flow(ticker)
        dow_flow[ticker] = flow
    except:
        error_symbols.append(ticker)

recent_sheets = {ticker : sheet.iloc[:,:1] for ticker, sheet in dow_balsheets.items()}
for ticker in recent_sheets.keys():
    recent_sheets[ticker].columns = ["Recent"]

recent_income_statements = {ticker : sheet.iloc[:,:1] for ticker,sheet in dow_income.items()}
for ticker in recent_income_statements.keys():
    recent_income_statements[ticker].columns = ["Recent"]

recent_cash_flows = {ticker : flow.iloc[:,:1] for ticker,flow in dow_flow.items()}
for ticker in recent_cash_flows.keys():
    recent_cash_flows[ticker].columns = ["Recent"]


combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()

combined_addstats = pd.concat(dow_addstats)
combined_addstats = combined_addstats.reset_index()

combined_balsheets = pd.concat(recent_sheets)
combined_balsheets = combined_balsheets.reset_index()

combined_income = pd.concat(recent_income_statements)
combined_income = combined_income.reset_index()

combined_flow = pd.concat(recent_cash_flows)
combined_flow = combined_flow.reset_index()

del combined_stats['level_1']
del combined_addstats['level_1']

combined_stats.columns = ['Ticker', 'Attribute', 'Recent']
combined_addstats.columns = ['Ticker', 'Attribute', 'Value']
combined_balsheets.columns = ['Ticker', 'Breakdown', 'Recent']
combined_income.columns = ["Ticker", "Breakdown", "Recent"]
combined_flow.columns = ["Ticker", "Breakdown", "Recent"]

# see fundamental stats
# get P/E ratio for each stock
df_per = combined_stats[combined_stats.Attribute.str.contains('Trailing P/E')]

# get P/S ratio for each stock
df_psr = combined_stats[combined_stats.Attribute.str.contains('Price/Sales')]

# get Price-to-Book ratio for each stock
df_pbr = combined_stats[combined_stats.Attribute.str.contains("Price/Book")]

# get PEG ratio for each stock
df_pegr = combined_stats[combined_stats.Attribute.str.contains('PEG')]

# get foward P/E ratio for each stock
df_fowper = combined_stats[combined_stats.Attribute.str.contains('Forward P/E')]

# see additional stats
# get ROE for each stock
df_roe = combined_addstats[combined_addstats.Attribute.str.contains('Return on Equity')]

# get ROA for each stock
df_roa = combined_addstats[combined_addstats.Attribute.str.contains('Return on Assets')]

# get profit margin for each stock
df_pm = combined_addstats[combined_addstats.Attribute.str.contains('Profit Margin')]

# see balance sheets
# get total assets
df_ta = combined_balsheets[combined_balsheets.Breakdown == 'totalAssets']

# See income statement
# get total revenue
df_tr = combined_income[combined_income.Breakdown == 'totalRevenue']

# see cash flow
# get dividends paid across companies
df_div = combined_flow[combined_flow.Breakdown == 'dividendsPaid']

# get stock issuance information
df_iss = combined_flow[combined_flow.Breakdown == 'isuuanceOfStock']

# merge dataframe
df = combined_stats
#df = pd.merge(df_per, df_psr, how='outer', on='Ticker')
#df = pd.merge(df, df_pbr, how='outer', on='Ticker')

print(df)
