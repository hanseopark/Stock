import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel

def main(url='', standard_symbol = '^IXIC', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    df = model.JudgeMarket(standard_symbol)

    df = df.reset_index()
    df = df.drop(['index', 'High', 'Low', 'Open', 'Close', 'Volume', 'Std', 'bol_upper', 'bol_down'], axis=1)
    strBull5 = df.loc[df.index[-1], 'JudgeMA5']
    strBull20 = df.loc[df.index[-1], 'JudgeMA20']
    strBull60 = df.loc[df.index[-1], 'JudgeMA60']
    strBull120 = df.loc[df.index[-1], 'JudgeMA120']

    if strBull5 == 'BullMarket':
        isBullMarket = True
    else:
        isBullMarket = False

#    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_BB'.format(end.date(), index_name)
#    df = pd.DataFrame(selected_BB, columns=['Ticker'])
#    df.to_json(url_trade+'.json')
#    df.to_csv(url_trade+'.csv')

    #print(df.loc[df.index[-1], :])

    df = model.with_moving_ave(standard_symbol)
    df = df['Adj Close']
    yearHigh = df.max(axis=0)
    recentValue = df.loc[df.index[-1]]

    print('Date range for bull or not')
    print('Start day: ', start, 'Last sunday: ', end)
    print('52weakHigh: ', yearHigh)
    print('Recent Value: ', recentValue)

    vari = (recentValue-yearHigh)/yearHigh * 100
    print('Variation of year: ', vari)

    if isBullMarket == True:
        print('\nCurrunt Bull Market in short term\n')
    else:
        print('\nCurrunt Bear Market in short term\n')

    return isBullMarket # True or False

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
    print('---------------------', filename, '------------------------')
    print('--------------------------------------------------')

    td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.date.today()
    last_sunday_offset = today.toordinal()%7
    last_sunday = today - datetime.timedelta(days=last_sunday_offset)
    start_day = today - td_1y

    main(url=root_url, standard_symbol = standard_index, index_list=dow_list, index_name=filename, start = start_day, end = last_sunday)
else:
    pass
