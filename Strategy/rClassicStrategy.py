import numpy as np
import pandas as pd
import yahoo_fin.stock_info as yfs

import matplotlib.pyplot as plt
import seaborn as sns
import json

from class_Strategy import LongTermStrategy

def PERStrategy(url, index_name, Limit = 10):
    strategy = LongTermStrategy(url, index_name)
    df_per = strategy.LowPER(threshold = Limit)
    df_per.sort_values(by='PER', inplace=True)

    return df_per

def PBRStrategy(url, index_name, Limit = 5):
    strategy = LongTermStrategy(url, index_name)
    df_pbr = strategy.LowPBR(threshold = Limit)

    return df_pbr

def main(url = '', index_name = 'dow', stat='', lim = 10):
    if stat == 'PER':
        df = PERStrategy(url, index_name, Limit=lim)
    elif stat == 'PBR':
        df = PBRStrategy(url, index_name, Limit=lim)

    print(df)

if __name__=='__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    dow_list = yfs.tickers_dow()
    filename= input("Choice of stock's list (dow, sp500, nasdaq, other, all, selected): ")
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
    elif filename == 'other':
        dow_list = yfs.tickers_other()
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()

    statements = input('Choice statement (PER, PBR): ')
    LimitValue = int(input('Set {} point example (10, 20, 30 ... ): '.format(statements)))

    main(url=root_url, index_name = filename, stat = statements, lim=LimitValue)

else:
    pass


