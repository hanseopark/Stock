import numpy as np
import pandas as pd

import json

from rClassicStrategy import PERStrategy, PBRStrategy
def LoadPortSP500(url = '', stat=''):
    url_trade = url+'data_ForTrading/'
    if stat == 'all':
        df = pd.read_json(url_trade+'sp500.json')
        port = df['Symbol'].values.tolist()
    else:
        df = pd.read_json(url_trade+'sp500_{}.json'.format(stat))
        port = df['Symbol'].values.tolist()

    return port

def LoadPort(url ='', stat=''):
    print('It is {} list'.format(stat))
    url_trade = url+'data_ForTrading/'
    if stat =='mine':
        f = open(url_trade+'MyPort.json', 'r')
    elif stat == 'watch':
        f = open(url_trade+'WatchPort.json', 'r')
    port = json.loads(f.read())

    while(True):
        print(port)
        s1 = input('add or del / exit\n')
        if s1 == 'exit':
            break
        elif s1 == 'add':
            s2 = input('To want to add ticker: / exit\n')
            if s2 == 'exit':
                break
            else:
                port.append(s2)
        else:
            s2 = input('To want to del ticker: / exit\n')
            if s2 == 'exit':
                break
            else:
                port.remove(s2)
    if stat == 'mine':
        with open (url_trade+'MyPort.json', 'w') as f:
            json.dump(port, f)
    elif stat == 'watch':
        with open (url_trade+'WatchPort.json', 'w') as f:
            json.dump(port, f)

    return port

def LoadClassicPort(url='', index_name='', Limit=10, stat=''):
    url_trade = url+'data_ForTrading/'
    if stat == 'lowper':
        df_per = PERStrategy(url,index_name,Limit)
        port = df_per.index.values.tolist()

    elif stat == 'lowpbr':
        df_pbr = PBRStrategy(url,index_name,Limit)
        port = df_pbr.index.values.tolist()

    return port

def main(url = ''):
    url_trade = url+'data_ForTrading/'

    ## Dow Index ##
    df_dow = pd.read_json(url_trade+'dow.json')

    ## S&P500 Index ##
    df_sp500 = pd.read_json(url_trade+'sp500.json')
    col_list = set(df_sp500['GICS Sector'].values.tolist())

    for col in col_list:
        df = df_sp500[df_sp500['GICS Sector']==col].copy()
        col = col.replace(' ', '_')
        df.to_json(url_trade+'sp500_{}.json'.format(col))

    ## Mine ##
    port_list = ['AAPL', 'TSM', 'TECL', 'BP', 'ZIM', 'MRO']
    with open (url_trade+'MyPort.json', 'w') as f:
        json.dump(port_list, f)

    ## Watchlist ##
    watch_list = ['SOXL, SOFI, APPS']
    with open (url_trade+'WatchPort.json', 'w') as f:
        json.dump(watch_list, f)

if __name__ == '__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    main(url=root_url)

else:
    pass

