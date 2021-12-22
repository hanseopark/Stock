import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel, FSModel

def CheckSafety():
    pass

    return True

def getTickerSafety(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'
    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)
    modelFS = FSModel(url_data, index_name, Offline=False)

    selected_SF = []
    error_symbols = []

    df = pd.DataFrame(index = index_list, columns=['marketCap', 'PER'])
    for ticker in tqdm(index_list):
        try:
            df.loc[ticker, 'marketCap'] = modelFS.getCap(ticker)
            df.loc[ticker, 'PER'] = modelFS.getPER(ticker)

        except:
            error_symbols.append(ticker)
    print('Except ticker: ',error_symbols)

    # Idea
    # 1. drop nan data
    df = df.dropna()
    return df

def main(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    selected_SF = []
    error_symbols = []
    tickers = getTickerSafety(url, index_list, index_name, start, end)
    print(tickers)

    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_SF'.format(end.date(), index_name)
    tickers.to_json(url_trade+'.json')
    tickers.to_csv(url_trade+'.csv')

    return(tickers)

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    print('\n****** Checking Safety of tickers ******')

    td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.datetime.now()
    start_day = today - td_1y

    filename = input('Using ticker list selected by BB, High, RSI model\n')
    url_BB = root_url+'/data_ForTrading/{0}/TickerList_{1}_High.json'.format(today.date(), filename)
    temp_pd = pd.read_json(url_BB)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

    print(dow_list)

    main(url=root_url, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
