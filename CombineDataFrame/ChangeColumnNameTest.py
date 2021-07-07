import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import json

def main():

    ## Nasdaq
    url_nasdaq = '/Users/hanseopark/Work/stock/data_origin/FS_nasdaq_'
    # Recent Price
    url_nasdaq_price = url_nasdaq+'Recent_Value.json'
    df_nasdaq_price = pd.read_json(url_nasdaq_price)

    # Stats
    url_nasdaq_stats = url_nasdaq+'stats.json'
    df_nasdaq_stats = pd.read_json(url_nasdaq_stats)

    # Addstats
    url_nasdaq_addstats = url_nasdaq+'addstats.json'
    df_nasdaq_addstats = pd.read_json(url_nasdaq_addstats)

    # Balsheets
    url_nasdaq_balsheets = url_nasdaq+'balsheets.json'
    df_nasdaq_balsheets = pd.read_json(url_nasdaq_balsheets)

    # Income
    url_nasdaq_income = url_nasdaq+'income.json'
    df_nasdaq_income = pd.read_json(url_nasdaq_income)

    # Cash flow
    url_nasdaq_flow = url_nasdaq+'flow.json'
    df_nasdaq_flow = pd.read_json(url_nasdaq_flow)

    ## other
    url_other = '/Users/hanseopark/Work/stock/data_origin/FS_other_'
    # Recent Price
#    url_other_price = url_other+'Recent_Value.json'
#    df_other_price = pd.read_json(url_other_price)

    # Stats
    url_other_stats = url_other+'stats.json'
    df_other_stats = pd.read_json(url_other_stats)

    # Addstats
    url_other_addstats = url_other+'addstats.json'
    df_other_addstats = pd.read_json(url_other_addstats)

    # Balsheets
    url_other_balsheets = url_other+'balsheets.json'
    df_other_balsheets = pd.read_json(url_other_balsheets)

    # Income
    url_other_income = url_other+'income.json'
    df_other_income = pd.read_json(url_other_income)

    # Cash flow
    url_other_flow = url_other+'flow.json'
    df_other_flow = pd.read_json(url_other_flow)

    filename = 'other'
    #list_stats = ['Recent_Value', 'stats', 'addstats', 'balsheets', 'income', 'flow']
    list_stats = ['stats', 'addstats', 'balsheets', 'income', 'flow']
    #list_stats = ['stats']
    for s in list_stats:
        url = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_{1}'.format(filename, s)
        if s == 'Recemt_Value':
            df = df_nasdaq_price
            #df = df.rename(columns={'level_0': 'Ticker'})
        if s == 'stats':
            df = df_nasdaq_stats
            df = df.rename(columns={'level_0': 'Ticker'})
        elif s == 'addstats':
            df = df_nasdaq_addstats
            df = df.rename(columns={'level_0': 'Ticker'})
        elif s == 'balsheets':
            df = df_nasdaq_balsheets
            df = df.rename(columns={'level_0': 'Ticker'})
        elif s == 'income':
            df = df_nasdaq_income
            df = df.rename(columns={'level_0': 'Ticker'})
        elif s == 'flow':
            df = df_nasdaq_flow
            df = df.rename(columns={'level_0': 'Ticker'})
        print(df)
#        df.to_json(url+'.json')
#        df.to_csv(url+'.csv')

if __name__ == '__main__':
    main()

else:
    pass
