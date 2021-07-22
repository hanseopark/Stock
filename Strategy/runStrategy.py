import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs
import matplotlib.pyplot as plt
import matplotlib.ticker as pltticker
import seaborn as sns

import json
import datetime

def main(url = '', index_list = ['AAPL'], index_name = 'dow', portfolio = ['AAPL'], stats = 'PER', Limit = 10):

    if stats == 'PER':
        from rClassicStrategy import PERStrategy
        df = PERStrategy(url,index_name, Limit)
        print(df)

    elif stats == 'PBR':
        from rClassicStrategy import PBRStrategy
        df = PBRStrategy(url,index_name, Limit)
        print(df)

    elif stats == 'Trend':
        from rTrendStrategy import main as TrendStrategy
        df = TrendStrategy(portfolio=port_list, start=start_day, end=today)
        print(df)

    elif stats == 'ML':
        from rMLStrategy import main as MLStrategy
        df = MLStrategy(url, index_list = dow_list, index_name=index_name, portfolio=port_list)
        print(df)

    elif stats == 'NLP':
        from rNLPStrategy import main as NLPStrategy
        title = NLPStrategy(url, index_name)
        print(title)

    ## SAVE ##
    url_trade  = url+'data_ForTrading/'
    df.to_json(url_trade+'{0}_{1}.json'.format(stats, index_name))
    df.to_csv(url_trade+'{0}_{1}.csv'.format(stats, index_name))

if __name__ == '__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)

    root_url = config['root_dir']
    dow_list = yfs.tickers_dow()
    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all, selected): ")
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

    from SettingPortpolio import LoadPortSP500, LoadPort, LoadClassicPort
    port_input = input('Set Portpolio: (sp500, dow, mine, watch, lowper) ')

    if port_input == 'sp500':
        df_sp500 = pd.read_json(root_url+'/data_ForTrading/{}.json'.format(port_input))
        col_list = str(set(df_sp500['GICS Sector'].values.tolist()))
        stat = input('Select sector in '+ col_list + ' and all: \n')
        port_list = LoadPortSP500(root_url, stat)
    elif port_input == 'lowper':
        port_list = LoadClassicPort(root_url, filename, 10, port_input)
    elif port_input == 'dow':
        port_list = yfs.tickers_dow()
    elif port_input == 'mine' or 'watch':
        port_list = LoadPort(root_url, port_input)
    else:
        port_list = LoadPort(root_url, 'mine')

    print('In my portfolio: ', port_list)

    LimitValue = 10
    statements = input('Choice statement (PER, PBR, Trend, ML, NLP): ')
    if (statements == 'PER' or statements == "PBR"):
        LimitValue = int(input('Set {} point(10, 20, 30): '.format(statements)))
    elif statements == 'Trend':
        td_1y = datetime.timedelta(weeks=52/2)
        today = datetime.datetime.now()
        start_day = today - td_1y
    else:
        LimitValue = 10

    main(url=root_url, index_list=dow_list, index_name = filename, portfolio = port_list, stats=statements, Limit=LimitValue)

else:
    pass

