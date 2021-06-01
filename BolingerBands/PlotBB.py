import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import gridspec
from mplfinance.original_flavor import candlestick2_ohlc

import datetime

from finance_class import Stocks

#pd.options.display.float_format = '{:.4f}'
#pd.set_option('display.max_columns', None)

td_1y = datetime.timedelta(weeks=52/2)
#start_day = datetime.datetime(2019,1,1)
#end_day = datetime.datetime(2021,5,1)
today = datetime.datetime.now()
start_day = today - td_1y

# To test just a ticker for making class
symbol = input('Write ticker name like aapl: ')

stock = Stocks(symbol, start_day, today)

# For figure
df = stock.with_moving_ave()
index = df.index.astype('str')
fig = plt.figure(figsize=(10,10))

gs = gridspec.GridSpec(2,1,height_ratios=[3,1])
ax_main = plt.subplot(gs[0])
ax_1 = plt.subplot(gs[1])

def x_date(x,pos):
    try:
        return index[int(x-0.5)][:7]
    except IndexError:
        return ''

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

#symbol = ['SPY', 'QQQ', 'IWD', 'GLD', 'SHY', 'IEF']

url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'

df_sp500 = pd.read_csv(url)




