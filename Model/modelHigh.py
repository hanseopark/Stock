import pandas as pd
import yahoo_fin.stock_info as yfs

import datetime
import json
from tqdm import tqdm

from classModel import priceModel, FSModel

def main(url='', index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    modelHigh = FSModel(url_data, index_name, Offline=False)
    modelBB = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    selected_High = []
    error_symbols = []

    for ticker in tqdm(index_list):
        try:
            high = float(modelHigh.getHigh(ticker))
            df_price = modelBB.get_price_data(ticker)
            df_recent = df_price.iloc[-1:]
            recent_price = float(df_recent['Adj Close'].item())
            ## Close 52 week high
            if (high - recent_price < 0.03*high):
                selected_High.append(ticker)
        except:
            error_symbols.append(ticker)
    print(error_symbols)

    url_trade = url+'/data_ForTrading/{0}/TickerList_{1}_High'.format(end.date(), index_name)
    df = pd.DataFrame(selected_High, columns=['Ticker'])
    df.to_json(url_trade+'.json')
    df.to_csv(url_trade+'.csv')

    print(df)
    return df

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.datetime.now()
    start_day = today - td_1y

    filename = input("Using ticker list selected by BB model\n")
    url_BB = root_url+'/data_ForTrading/{0}/TickerList_{1}_BB.json'.format(today.date(), filename)
    temp_pd = pd.read_json(url_BB)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

    print(dow_list)

    main(url=root_url, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
