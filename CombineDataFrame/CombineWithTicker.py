import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import datetime
import json

def main(url='', index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_trade = url+'data_ForTrading/{0}/'.format(end.date())
    print('Checking stability of company')
    print('If ticked is selected in Dow and S*P500 index, it has already been checked for safety')
    indexs = ['dow', 'sp500']
    select = set()
    res = []
    # Dow ,S&P500
    for index in indexs:
        df = pd.read_json(url_trade+'TickerList_{}_High.json'.format(index))
        tickers = set(df['Ticker'].values.tolist())
        select.update(tickers)
    res=list(select)

#   It is need to think how to check company safety
#    # Nasdaq
#    df = pd.read_json(url_trade+'TickerList_nasdaq_High.json')
#    tickers = df['Ticker'].values.tolist()
#
#    # Other
#    df = pd.read_json(url_trade+'TickerList_other_High.json')
#    tickers = df['Ticker'].values.tolist()

    if select:
        print(res)
        with open(url_trade+'TickerList.json', 'w') as f:
            json.dump(res, f)
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
