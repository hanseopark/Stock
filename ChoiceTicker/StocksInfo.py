import pandas as pd
import yahoo_fin.stock_info as yfs

import json

def main (url, df_index, index_list, index_name):

    ## Configuration directory url
    url_trade  = url+'data_ForTrading/'

    ## SAVE ##
    df_index.to_json(url_trade+'{0}.json'.format(index_name))
    df_index.to_csv(url_trade+'{0}.csv'.format(index_name))

if __name__ == '__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename= input("Choice of stock's list (dow, sp500, nasdaq, other): ")

    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        df_dow = yfs.tickers_dow(True)
        dow_list = df_dow['Symbol'].values.tolist()
    elif filename == 'sp500':
        df_dow = yfs.tickers_sp500(True)
        dow_list = df_dow['Symbol'].values.tolist()
    elif filename == 'nasdaq':
        df_dow = yfs.tickers_nasdaq(True)
        df_dow.drop(df_dow.index[-1], inplace=True) # File creation
        dow_list = df_dow['Symbol'].values.tolist()
    elif filename == 'other':
        df_dow = yfs.tickers_other(True)
        df_dow.drop(df_dow.index[-1], inplace=True) # File creation
        dow_list = df_dow['NASDAQ Symbol'].values.tolist()

    print(df_dow)
    print(dow_list)

    main(url=root_url, df_index = df_dow, index_list = dow_list, index_name=filename)

else:
    pass
