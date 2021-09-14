import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import daterange, priceModel
from modelBB import getTickerBB, ConditionBB
from modelBull import main as isBull

def main(url='', standard_symbol = '^IXIC',index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    # 1. Buying strategy
    # Choice about ticker in condition
    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    df = pd.DataFrame(columns=['Ticker'])
    period = 7
    for dt in tqdm(daterange(start, end, period)):
        tickers = getTickerBB(url, standard_symbol, index_list, index_name, start, dt+datetime.timedelta(period))
        df.loc[dt, 'Ticker'] = tickers['Ticker'].values.tolist()
        #print('ticker: ', tickers['Ticker'].values.tolist())
        #print(df)

    # 2. Selling strategy
    # When do it buy what's point
    cash = 1000000
    for dt in df.index:
        tickers = df.loc[dt, 'Ticker']
        if len(tickers) == 0:
            continue
        else:
            eachCash = cash/len(tickers)
            cash_arr = []
            for ticker in tickers:
                # 2-1 RSI
    #            model = priceModel(url_data, index_name, dt, end, Offline=False, run_yfs=True)
    #            df_RSI = model.calcRSI(ticker)
    #            print(df_RSI)

                # 2-2 Weekly
                model = priceModel(url_data, index_name, dt+datetime.timedelta(days=1), dt+datetime.timedelta(weeks=1), Offline=False, run_yfs=True)
                df_price = model.get_price_data(ticker)
                df_ago = df_price.iloc[:1]
                df_rec = df_price.iloc[-1:]
                price_ago = df_ago['Open'].item()
                price_rec = df_rec['Adj Close'].item()

                # Wallet
                numTicker = eachCash // price_ago
                cash_arr.append(eachCash + numTicker*(price_rec-price_ago))
            cash = sum(cash_arr)

            # 2-3 daily
            #model = priceModel(url_data, index_name, dt+datetime.timedelta(days=1), dt+datetime.timedelta(days=1), Offline=False, run_yfs=True)

    print('Cash: ', cash)
    print('Growth rate: ', (cash-1000000)/1000000 * 100,'%')

    # For comparing index
    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)
    df_std = model.get_price_data(standard_symbol)
    df_ago = df_std.iloc[:1]
    df_rec = df_std.iloc[-1:]
    price_ago = df_ago['Open'].item()
    price_rec = df_rec['Adj Close'].item()

    print('Growth rate about index: ', (price_rec-price_ago)/price_ago * 100,'%')

    return(tickers)

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all): \n")
    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
        standard_index = '^DJI'
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
        standard_index = '^GSPC'
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
        standard_index = '^IXIC'
    elif filename == 'other':
        dow_list = yfs.tickers_other()
        standard_index = '^IXIC'
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
        standard_index = '^IXIC'
    print('--------------------------------------------------')
    print('-----------------', filename, '-------------------')
    print('--------------------------------------------------')

    start_day = datetime.datetime(2010,1,2) # must be Sun day
    today = datetime.datetime.now()

    main(url=root_url, standard_symbol = standard_index, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
