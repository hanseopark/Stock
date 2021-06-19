import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import gridspec
from mplfinance.original_flavor import candlestick2_ohlc

import datetime

def main(symbol='AAPL', offline_test=False, SelectStrategy='BB', day_init=datetime.datetime(2019,1,1), today=datetime.datetime.now()):
    # To test just a ticker for making class
    url_data = '/Users/hanseopark/Work/stock/data_origin/'

    stock = ShortTermStrategy(symbol, day_init, today, url=url_data, Offline= offline_test)

    ## For figure
    if SelectStrategy == 'BB':
        df = stock.with_moving_ave()
    elif SelectStrategy == 'RSI':
        df = stock.calcRSI()

    index = df.index.astype('str')
    fig = plt.figure(figsize=(10,10))

    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except IndexError:
            return ''

    if SelectStrategy == 'BB':
        gs = gridspec.GridSpec(2,1,height_ratios=[3,1])
        ax_main = plt.subplot(gs[0])
        ax_1 = plt.subplot(gs[1])
        # ax_main
        ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

        ax_main.set_title(symbol+' stock', fontsize=22 )

        #ax_main.set_xlabel('Date')
        ax_main.plot(index, df['MA5'], label='MA5')
        ax_main.plot(index, df['MA20'], label='MA20')
        ax_main.plot(index, df['MA60'], label='MA60')
        ax_main.plot(index, df['MA120'], label='MA120')
        ax_main.plot(index, df['bol_upper'], label='bol_upper')
        ax_main.plot(index, df['bol_down'], label='bol_down')
        ax_main.fill_between(index, df['bol_down'], df['bol_upper'], color = 'gray')

        candlestick2_ohlc(ax_main,df['Open'],df['High'],df['Low'],df['Close'], width=0.5, colorup='r', colordown='b')

        ax_main.legend(loc=2)

        # ax_1
        ax_1.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax_1.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))
        ax_1.set_xlabel('Date')
        ax_1.set_ylabel('Std')
        ax_1.plot(index, df['Std'], label='Std')
        mean = df['Std'].mean()
        ax_1.hlines(y=mean, xmin=index[0], xmax=index[-1], colors='red')

        plt.grid()
        plt.show()

    elif SelectStrategy == 'RSI':
        ax_main = plt.subplot(1,1,1)
        ax_main.set_title(symbol+' stock', fontsize=22 )
        ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

        ax_main.plot(index, df['RSI'], label='RSI')
        ax_main.plot(index, df['RSI signal'], label='RSI signal')
        ax_main.legend(loc=2)

        plt.grid()
        plt.show()

    else:
        pass

    return fig

if __name__ == '__main__':
    from class_Strategy import ShortTermStrategy
    symbol = input('Write ticker name like AAPL: ')
    offline_test = bool(input('Do you want offline test? (t/f): ') == 't')
    SelectStrategy = input('What do you want to choose the strategy (BB, RSI): ')

    td_1y = datetime.timedelta(weeks=52/2)
    #start_day = datetime.datetime(2019,1,1)
    #end_day = datetime.datetime(2021,5,1)
    today = datetime.datetime.now()
    start_day = today - td_1y

    main(symbol, offline_test, SelectStrategy, start_day, today)
else:
    from Strategy.class_Strategy import ShortTermStrategy



