import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel

def CheckSafety(ma5, ma20, ma60, ma120, upper, down, value, within, close):
    if ma5>=ma20 and ma20>=ma60 and ma60>=ma120: # MACD
        if (upper-down) < ma20 * within: # within 15%
            if 0 < upper - value < close: # Close to the upper band
                return True

def getTickerSafety(url='', standard_symbol = '^IXIC',index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'
    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)
    selected_BB = []
    error_symbols = []

    withIn = 0.4 # default 0.4, 20%
    Close = 0.015 # default 0.015, 1.5%
    print('Date range: ', start, ' to ', end)
    print('Condition within: ', withIn)
    print('Condition close: ', Close)

    for ticker in tqdm(index_list):
        try:
            df_BB = model.with_moving_ave(ticker)
            df_recent = df_BB.iloc[-1:]
            value_recent = float(df_recent['Adj Close'])
            upper_recent = float(df_recent['bol_upper'])
            down_recent = float(df_recent['bol_down'])
            ma5 = float(df_recent['MA5'])
            ma20 = float(df_recent['MA20'])
            ma60 = float(df_recent['MA60'])
            ma120 = float(df_recent['MA120'])

            # Modeling idea
            if ConditionBB(ma5, ma20, ma60, ma120, upper_recent, down_recent, value_recent, withIn, Close):
                selected_BB.append(ticker)
        except:
            error_symbols.append(ticker)
    print('Except ticker: ',error_symbols)

    df = pd.DataFrame(selected_BB, columns=['Ticker'])

    return df

def main(url='', standard_symbol = '^IXIC',index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    selected_BB = []
    error_symbols = []
    tickers = getTickerSafety(url, standard_symbol, index_list, index_name, start, end)
    print(tickers)

    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_BB'.format(end.date(), index_name)
    tickers.to_json(url_trade+'.json')
    tickers.to_csv(url_trade+'.csv')

    return(tickers)

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    print('\n****** Checking Safety of tickers ')

    td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.datetime.now()
    start_day = today - td_1y

    filename = input('Using ticker list selected by BB, High, RSI model\n')
    url_BB = root_url+'/data_ForTrading/{0}/TickerList_{1}_RSI.json'.format(today.date(), filename)
    temp_pd = pd.read_json(url_BB)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

    print(dow_list)

    main(url=root_url, standard_symbol = standard_index, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
