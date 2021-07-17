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
    #######################################################
    # Select strategy for situation
    if (stats == 'PER' or stats == "PBR"):
        strategy = LongTermStrategy(url, index_name) # Select Long term strategy
    elif stats == 'NLP':
        strategy = NLPStrategy(url, index_name, Offline= True) # Select Long term strategy
        #strategy = NLPStrategy(url, index_name, Offline= False) # Select Long term strategy

    # Perform strategy and save
    url_threshold = url+'/data_origin/table{0}_{1}_{2}'.format(stats, index_name, Limit)
    if stats == 'PER':
        df_per = strategy.LowPER(threshold = Limit)
        #print(df_per)
        df_per.to_json(url_threshold+'.json')
        df_per.to_csv(url_threshold+'.csv')
        print(df_per)

        return df_per

    elif stats == 'PBR':
        df_pbr = strategy.LowPBR(threshold = Limit)
        #print(df_pbr)
        df_pbr.to_json(url_threshold+'.json')
        df_pbr.to_csv(url_threshold+'.csv')

        print(df_pbr)

        return df_pbr

    elif stats == 'Trend':
        from TrendStrategy import main as TrendStrategy
        df = TrendStrategy(portfolio=port_list, start=start_day, end=today)
        print(df)

    elif stats == 'ML':
        from MLStrategy import main as MLStrategy
        sub = MLStrategy(url, index_list = dow_list, index_name=index_name, portfolio=port_list)
        print(sub)

    elif stats == 'NLP':
        ## Test ##
        title = strategy.get_news_title()
        print(title)

if __name__ == '__main__':
    from class_Strategy import LongTermStrategy, NLPStrategy

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

    port_input = input('set portpolio: (lowper, energy, mine) ')
    if port_input == 'energy':
        energy_list = ['APA', 'COG', 'COP', 'CVX', 'DVN', 'EOG', 'FANG', 'HAL', 'HES', 'KMI', 'MPC', 'MRO', 'NOV', 'OKE', 'OXY', 'PSX', 'PXD', 'SLB', 'VLO', 'WMB', 'XOM']
        port_list = energy_list
    elif port_input == 'lowper':
        df_low_per = main(stock_list=filename, stats = 'PER', Limit = 5)
        lowper_list = df_low_per.index.values.tolist()
        port_list = lowper_list
    elif port_input == 'mine':
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list
    else:
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list

    print('In my portfolio: ', port_list)

    LimitValue = 10
    statements = input('Choice statement (PER, PBR, Trend, ML, NLP): ')
    if (statements == 'PER' or statements == "PBR"):
        s2 = input('Set {} point(10, 20, 30): '.format(statements))
        LimitValue = int(s2)
    elif statements == 'Trend':
        td_1y = datetime.timedelta(weeks=52/2)
        today = datetime.datetime.now()
        start_day = today - td_1y
    else:
        LimitValue = 10

    main(url=root_url, index_list=dow_list, index_name = filename, portfolio = port_list, stats=statements, Limit=LimitValue)

else:
    from Strategy.class_Strategy import LongTermStrategy, TrendStrategy
#    s_list= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
#    statements = input('Choice statement (PER, PBR, Trend, ML): ')
#    main(stock_list=s_list, stats=statements)









