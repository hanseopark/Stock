import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel

def main(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    selected_RSI = []
    error_symbols = []

    down = 40
    print('Condition to get ticker about point below :', down)

    for ticker in tqdm(index_list):
        try:
            df = model.calcRSI(ticker)
            df_recent = df.iloc[-1:]
            value_RSI = float(df_recent['RSI'])
            value_RSI_signal = float(df_recent['RSI signal'])
            if value_RSI < down:
                if value_RSI < value_RSI_signal:
                    selected_RSI.append(ticker)
        except:
            error_symbols.append(ticker)
    print(error_symbols)

    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_RSI'.format(today.date(), index_name)
    df = pd.DataFrame(selected_RSI, columns=['Ticker'])
    df.to_json(url_trade+'.json')
    df.to_csv(url_trade+'.csv')

    print(df)
    return df

if __name__ == '__main__':
    print('\n')
    print('************* Comparing RSI point ***************')
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    td_1y = datetime.timedelta(weeks=52)
    today = datetime.datetime.now()
    start_day = today - td_1y

    filename = input("Using ticker list selected by BB and High model\n")
    url_BB = root_url+'/data_ForTrading/{0}/TickerList_{1}_High.json'.format(today.date(), filename)
    temp_pd = pd.read_json(url_BB)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

    print(dow_list)

#    s = input('what is strategy ? (BB, Corona) ')
#    if s == 'BB':
#        url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList.json'.format(today.date())
#        s_list = pd.read_json(url)['Ticker'].values.tolist()
#    elif s == 'Corona':
#        url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList_corona.json'.format(today.date())
#        s_list = pd.read_json(url).index
#
#    else:
#        url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList.json'.format(today.date())
#        s_list = pd.read_json(url)['Ticker'].values.tolist()

    main(url=root_url, index_list=dow_list, index_name=filename, start = start_day, end = today)

else:
    pass
