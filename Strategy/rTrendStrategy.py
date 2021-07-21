import numpy as np
import pandas as pd
import yahoo_fin.stock_info as yfs

import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import json

from class_Strategy import TrendStrategy
def main(portfolio=['AAPL'], start=datetime.datetime.now(), end=datetime.datetime.now()):

    ticker = portfolio[0]
    strategy = TrendStrategy(symbol=ticker, start= start, end= end)

    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except indexerror:
            return ''

    df_price = strategy.get_price_data(nomalization = True)
    df_tr = strategy.get_trend_data()
    df = pd.concat([df_price, df_tr], axis=1)

    ## Figure
    index = df_price.astype('str')
    fig = plt.figure(figsize=(10,10))
    ax_main = plt.subplot(1,1,1)
    ax_main.set_title("Stock's value with google trend", fontsize=22 )
    ax_main.plot(df_price, label="Stock's value")
    ax_main.plot(df_tr, label = 'Trend')
    ax_main.legend(loc=2)

    plt.grid()
    plt.show()

    #print(df)

    return df

if __name__ == '__main__':
    port_input = input('set portpolio: (lowper, energy, mine) ')
    if port_input == 'energy':
        energy_list = ['APA', 'COG', 'COP', 'CVX', 'DVN', 'EOG', 'FANG', 'HAL', 'HES', 'KMI', 'MPC', 'MRO', 'NOV', 'OKE', 'OXY', 'PSX', 'PXD', 'SLB', 'VLO', 'WMB', 'XOM']
        port_list = energy_list
    elif port_input == 'lowper':
        df_low_per = main(stock_list=filename, stats = 'PER', Limit = 5)
        lowper_list = df_low_per.index.values.tolist()
        port_list = lowper_list
    elif port_input == 'mine':
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list
    else:
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list

    print('In my portfolio: ', port_list)

    td_1y = datetime.timedelta(weeks=52/2)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(portfolio = port_list, start=start_day, end=today)

else:
    pass


