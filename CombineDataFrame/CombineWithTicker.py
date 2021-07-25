import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import matplotlib as plt
import seaborn as sns
import datetime
import json

def main(url='', index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_trade = url+'data_ForTrading/{0}/'.format(end.date())
    indexs = ['dow', 'sp500', 'nasdaq']
    select = set()
    for index in indexs:
        df = pd.read_json(url_trade+'TickerList_{}.json'.format(index))
        tickers = set(df['Ticker'].values.tolist())
        select.update(tickers)

    if select:
        print(list(select))
        with open(url_trade+'TickerList.json', 'w') as f:
            json.dump(list(select), f)
    else:
        print('Ticker is not found')

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    td_1y = datetime.timedelta(weeks=52/2)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(url=root_url,start=start_day, end=today)
else:
    pass
