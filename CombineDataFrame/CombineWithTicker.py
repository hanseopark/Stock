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

    filename = 'all'
    list_stats = ['stats', 'addstats', 'balsheets', 'income', 'flow']
    #list_stats = ['stats']
    for s in list_stats:
        url = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_{1}'.format(filename, s)
        if s == 'Recemt_Value':
            df = pd.concat([df_nasdaq_price, df_other_price], join='outer')
            df = df.reset_index()
            del df['index']
        if s == 'stats':
            df = pd.concat([df_nasdaq_stats, df_other_stats])
            df = df.reset_index()
            del df['index']
        elif s == 'addstats':
            df = pd.concat([df_nasdaq_addstats, df_other_addstats])
            df = df.reset_index()
            del df['index']
        elif s == 'balsheets':
            df = pd.concat([df_nasdaq_balsheets, df_other_balsheets])
            df = df.reset_index()
            del df['index']
        elif s == 'income':
            df = pd.concat([df_nasdaq_income, df_other_income])
            df = df.reset_index()
            del df['index']
        elif s == 'flow':
            df = pd.concat([df_nasdaq_income, df_other_income])
            df = df.reset_index()
            del df['index']
        print(df)
        print(df.dtypes)
#        df.to_json(url+'.json')
#        df.to_csv(url+'.csv')

    url = '/Users/hanseopark/Work/stock/data_ForTrading/all_ticker.json'
    df_tic = pd.DataFrame(columns=['Ticker'])
    df_tic['Ticker'] = df['Ticker']
    print('ticker')
    print(df_tic)
#    df.to_json(url)

if __name__ == '__main__':
    main()

else:
    pass
