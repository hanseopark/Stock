import datetime
import os.path
import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import gridspec
import seaborn as sns

from tqdm import tqdm
import json
import datetime
from class_Strategy import LongTermStrategy

print('It is true strategy of low PER is right?')

def main(url = '', standard_name = '^DJI', index_list = ['AAPL'], index_name = 'dow', stats = 'PER', start=datetime.datetime.now(), end=datetime.datetime.now()):
    url_trade  = url+'data_ForTrading/'
    df = pd.read_json(url_trade+'{0}_{1}.json'.format(stats, index_name))
    df.sort_values(by='PER', inplace=True)
    print(df)
    selected_ticker = df.index.values.tolist()
    print(selected_ticker)

    df_st = pdr.DataReader(standard_name,'yahoo', start_day, today)
    init_st_price = df_st.loc[df_st.index[0], 'Adj Close']
    last_st_price = df_st.loc[df_st.index[-1], 'Adj Close']
    df_st['Adj Close'] = df_st['Adj Close']/init_st_price # Normalization
    return_st_price = (last_st_price/init_st_price)
    print('Variance of index: ', return_st_price)

    # Figure
    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(2,1,height_ratios=[1,1])
    ax_main = plt.subplot(gs[0])
    ax_1 = plt.subplot(gs[1])
    index = df_st.index.astype('str')
    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except IndexError:
            return ''
    ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

    list_return = []
    # ax_main
    ax_main.plot(index, df_st['Adj Close'], color='r', linestyle='solid', label='Dow index (^DJI)')
    for tic in selected_ticker:
        df_price = pdr.DataReader(tic,'yahoo', start_day, today)
        init_price = df_price.loc[df_price.index[0], 'Adj Close']
        last_price = df_price.loc[df_price.index[-1], 'Adj Close']
        df_price['Adj Close'] = df_price['Adj Close']/init_price # Normalization
        return_price = (last_price/init_price)
        if return_price > return_st_price:
            ax_main.plot(index, df_price['Adj Close'], linestyle='solid', label=tic)
        else:
            ax_main.plot(index, df_price['Adj Close'], linestyle='dotted', label=tic)
        print('Variance of {0}: '.format(tic), return_price)
        list_return.append(return_price)
    ax_main.legend(loc=2)

    # ax_1
    ax_1.bar(selected_ticker, list_return, color='darkgray')
    ax_1.set_ylabel('Return (Last Price / Initial Price)')
    ax_1.axhline(y=return_st_price, color='r', label=standard_name)
    ax_1.axhline(y=sum(list_return)/len(list_return), color='g', label='Mean of tickers')
    ax_1.legend(loc=2)

    plt.show()

if __name__ == '__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    dow_list = yfs.tickers_dow()
    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all, selected): ")
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
        standard_index = '^DJI'
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
        standard_index = '^DJI'
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
        standard_index = '^DJI'
    elif filename == 'other':
        dow_list = yfs.tickers_other()
        standard_index = '^DJI'
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
        standard_index = '^DJI'
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()
        standard_index = '^DJI'

    statements = input('Choice statement (PER, PBR, Trend, ML, NLP, Port): ')

    td_1y = datetime.timedelta(weeks=52/2)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(url=root_url, standard_name = standard_index, index_list=dow_list, index_name = filename, stats=statements, start=start_day, end=today)

else:
    pass

