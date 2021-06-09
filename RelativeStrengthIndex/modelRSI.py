import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime
from tqdm import tqdm

from classRSI import Stocks

td_1y = datetime.timedelta(weeks=52/2)
today = datetime.datetime.now()
start_day = today - td_1y

url = '/Users/hanseopark/Work/stock/data_ForTrading/{0}_TickerList.json'.format(today.date())
stock_list = pd.read_json(url)['Ticker'].values.tolist()
print(stock_list)

selected_ticker = []
for ticker in tqdm(stock_list):
    stock = Stocks(ticker, start_day, today)
    df = stock.calcRSI()
    df_recent = df.iloc[-1:]
    value_RSI = float(df_recent['RSI'])
    value_RSI_signal = float(df_recent['RSI signal'])
    if value_RSI < 40:
        if value_RSI < value_RSI_signal:
            selected_ticker.append(ticker)

print(selected_ticker)

url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
df = pd.DataFrame(selected_ticker, columns=['Ticker'])
df.to_json(url)
