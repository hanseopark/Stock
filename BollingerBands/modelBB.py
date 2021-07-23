import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classBB import Stocks

def main(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    selected_ticker = []
    url_data = url+'data_origin/'
    for ticker in tqdm(index_list):
        stock = Stocks(url_data, ticker, index_name, start, end)
        df_price = stock.get_price_data()
        df = stock.with_moving_ave()
        index = df.index.astype('str')
        mean = df['Std'].mean()
        df_day_ago_ago = df.iloc[-3]
        df_day_ago = df.iloc[-2]
        df_recent = df.iloc[-1:]
        value_day_ago_ago = float(df_day_ago_ago['Adj Close'])
        value_day_ago = float(df_day_ago['Adj Close'])
        value_recent = float(df_recent['Adj Close'])
        upper_recent = float(df_recent['bol_upper'])
        down_recent = float(df_recent['bol_down'])
        std_recent = float(df_recent['Std'])

        if std_recent < mean and value_recent > value_day_ago and value_day_ago > value_day_ago_ago and value_recent < upper_recent:
            selected_ticker.append(ticker)

    url_trade = url+'/data_ForTrading/{0}/TickerList_BB'.format(today.date())
    df = pd.DataFrame(selected_ticker, columns=['Ticker'])
    df.to_json(url_trade+'.json')
    df.to_csv(url_trade+'.csv')

    print(df)
    return df

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename = input("Choice of stock's list (dow, sp500, nasdaq, other): ")
    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
    elif filename == 'other':
        dow_list = yfs.tickers_other()
    print(dow_list)

    td_1y = datetime.timedelta(weeks=52/2)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(url=root_url, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
