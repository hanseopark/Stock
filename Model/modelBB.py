import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel

def main(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    selected_BB = []
    error_symbols = []
    for ticker in tqdm(index_list):
        try:
            df_price = model.get_price_data(ticker)
            df_BB = model.with_moving_ave(ticker)
            index = df_BB.index.astype('str')
            mean = df_BB['Std'].mean()
            df_day_ago_ago = df_BB.iloc[-3]
            df_day_ago = df_BB.iloc[-2]
            df_recent = df_BB.iloc[-1:]
            value_day_ago_ago = float(df_day_ago_ago['Adj Close'])
            value_day_ago = float(df_day_ago['Adj Close'])
            value_recent = float(df_recent['Adj Close'])
            upper_recent = float(df_recent['bol_upper'])
            down_recent = float(df_recent['bol_down'])
            std_recent = float(df_recent['Std'])
            ma5 = float(df_recent['MA5'])
            ma20 = float(df_recent['MA20'])
            ma60 = float(df_recent['MA60'])
            ma120 = float(df_recent['MA120'])

            # Modeling idea
            # MACD
            if ma5>ma20 and ma20>ma60 and ma60>ma120:
                # within 15%
                if (upper_recent-down_recent) < ma20*0.3:
                    # Close to the upper band
                    if 0< upper_recent - value_recent < 0.015:
                        selected_BB.append(ticker)
        except:
            error_symbols.append(ticker)
    print(error_symbols)

    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_BB'.format(end.date(), index_name)
    df = pd.DataFrame(selected_BB, columns=['Ticker'])
    df.to_json(url_trade+'.json')
    df.to_csv(url_trade+'.csv')

    print(df)
    return df

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all): \n")
    dow_list = yfs.tickers_dow()
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
    print('--------------------------------------------------')
    print('-----------------', filename, '-------------------')
    print('--------------------------------------------------')

    td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(url=root_url, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
