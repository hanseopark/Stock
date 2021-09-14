import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from class_Strategy import ShortTermStrategy

def daterange(start_date, end_date, step):
    end_date = end_date-5*datetime.timedelta(step)
    for n in range(0, int((end_date-start_date).days) +1, step):
        yield start_date+datetime.timedelta(n)

def main(url='', standard_symbol = '^IXIC', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = ShortTermStrategy(standard_symbol, start, end, url_data, Offline=False, run_yfs=True)

    df = model.JudgeMarket()

    period = 7

    CountTrue = 0
    CountFalse = 0
    for dt in tqdm(daterange(start, end, period)):
        df_cond = df.loc[dt:dt+datetime.timedelta(period)]
        df_cond_recent = df_cond.iloc[-1:]
        df_result = df.loc[dt+datetime.timedelta(period): dt+datetime.timedelta(2*period)]
        df_result_ago = df_result.iloc[0:1]
        df_result_recent = df_result.iloc[-1:]
        agoValue = float(df_result_ago['Open'].item())
        recentValue = float(df_result_recent['Adj Close'].item())

        strBull5 = df_cond_recent['JudgeMA5'].item()

        if strBull5 == 'BullMarket':
            isBullMarket = True
        else:
            isBullMarket = False

        if isBullMarket == bool(recentValue - agoValue > 0):
            CountTrue +=1
        else:
            CountFalse +=1

    print('True: ', CountTrue)
    print('False: ', CountFalse)

    return 0 # True or False

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

    #td_1y = datetime.timedelta(weeks=52*3)
    #start_day = datetime.datetime(2000,1,2)
    start_day = datetime.datetime(2010,1,3)
    today = datetime.datetime.now()
    #start_day = today - td_1y

    main(url=root_url, standard_symbol = standard_index, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
