import numpy as np
import pandas as pd
import yahoo_fin.stock_info as yfs
import pandas_datareader as pdr

import datetime
from tqdm import tqdm

def main(stock_list=['dow']):
    # Get datetime for price of stock
    covid_day_ago = datetime.datetime(2020,2,19)
    temp_day = datetime.datetime(2020,3,18)
    covid_day = datetime.datetime.strftime(temp_day, '%Y-%m-%d')
    today = datetime.datetime.now()

    # Get list of Dow tickers
    dow_list = yfs.tickers_dow()
    filename = ''
    if stock_list == 'dow':
        dow_list = yfs.tickers_dow()
        filename = 'dow'
    elif stock_list == 'sp500':
        filename = 'sp500'
        dow_list = yfs.tickers_sp500()
    elif stock_list == 'nasdaq':
        filename = 'nasdaq'
        dow_list = yfs.tickers_nasdaq()
    elif stock_list == 'other':
        filename = 'other'
        dow_list = yfs.tickers_other()
    elif stock_list == 'selected':
        filename = 'selected'
        url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()

    print('*'*100)
    print(dow_list)
    print('*'*100)

    df_price_nasdaq = pdr.DataReader('^IXIC', 'yahoo', covid_day_ago, today)
    df_day_covid_ago = df_price_nasdaq.iloc[0]
    df_day_covid = df_price_nasdaq.loc[covid_day]
    df_day_today  = df_price_nasdaq.iloc[-1]
    price_covid_ago = float(df_day_covid_ago['Adj Close'])
    price_covid = float(df_day_covid['Adj Close'])
    price_today = float(df_day_today['Adj Close'])
    disc_before = price_covid / price_covid_ago -1
    disc_after = price_today / price_covid
    print('Discrimination before corona: ',disc_before)
    print('Discrimination after corona: ',disc_after)
    print(price_covid_ago, price_covid, price_today)

    df_res = pd.DataFrame(columns=['ratio_before', 'ratio_after', 'covid_day', 'today'])
    df_res_out = pd.DataFrame(columns=['ratio_before', 'ratio_after', 'covid_day', 'today'])
    error_symbols = []

    for ticker in tqdm(dow_list):
        try:
            df_price = pdr.DataReader(ticker, 'yahoo', covid_day_ago, today)
            df_day_covid_ago = df_price.iloc[0]
            df_day_covid = df_price.loc[covid_day]
            df_day_today  = df_price.iloc[-1]
            price_covid_ago = float(df_day_covid_ago['Adj Close'])
            price_covid = float(df_day_covid['Adj Close'])
            price_today = float(df_day_today['Adj Close'])
            disc_before_ticker = price_covid / price_covid_ago -1
            disc_after_ticker = price_today / price_covid
            #if disc_after > disc_after_ticker and disc_before < disc_before_ticker:
            if abs(disc_before_ticker) > abs (disc_before) and disc_after_ticker < disc_after:
                df_res.loc[ticker,'ratio_before'] =disc_before_ticker
                df_res.loc[ticker,'ratio_after'] =disc_after_ticker
                df_res.loc[ticker,'covid_day'] = price_covid
                df_res.loc[ticker,'today'] = price_today
            else:
                df_res_out.loc[ticker,'ratio_before'] = disc_before_ticker
                df_res_out.loc[ticker,'ratio_after'] = disc_after_ticker
                df_res_out.loc[ticker,'covid_day'] = price_covid
                df_res_out.loc[ticker,'today'] = price_today
        except:
            error_symbols.append(ticker)

    df_res = df_res.sort_values('ratio_after', ascending=True)
    df_res_out = df_res_out.sort_values('ratio_after', ascending=False)
    print('#'*10)
    print('### '+'IN'+' ###')
    print('#'*10)
    print(df_res)
    print('#'*11)
    print('### '+'OUT'+' ###')
    print('#'*11)
    print(df_res_out)
    selected_ticker = df_res.index
    url = '/Users/hanseopark/Work/stock/' # in data
    strategy = LongTermStrategy(url, filename) # Select Long term strategy
    df_stats = strategy.get_stats(preprocessing = True)
    df_res = df_res.join(df_stats).copy()

    # detail condition
    df_res = df_res[df_res['PER'] < 20]
    df_res = df_res[df_res['forPER'] < df_res['PER']]

    print(df_res)
    url_res = url+'/data_ForTrading/{0}_TickerList_corona'.format(today.date())
    df_res.to_json(url_res+'.json')
    df_res.to_csv(url_res+'.csv')

    return df_res

if __name__ == '__main__':
    from class_Strategy import LongTermStrategy, TrendStrategy, NLPStrategy
    s_list= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
    main(stock_list=s_list)

else:
    pass
