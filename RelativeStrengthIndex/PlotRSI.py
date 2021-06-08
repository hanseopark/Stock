import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from classRSI import Stocks

td_1y = datetime.timedelta(weeks=52/2)
today = datetime.datetime.now()
start_day = today - td_1y

symbol = input('Write ticker name like aapl: ')

stock = Stocks(symbol, start_day, today)

df= stock.calcRSI()

#print(df)

index = df.index.astype('str')

fig = plt.figure(figsize=(10,10))

ax_main = plt.subplot(1,1,1)

def x_date(x,pos):
    try:
        return index[int(x-0.5)][:7]
    except IndexError:
        return ''

# For figure
ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

ax_main.plot(index, df['RSI'], label='RSI')
ax_main.plot(index, df['RSI signal'], label='RSI signal')

plt.grid()
plt.show()


