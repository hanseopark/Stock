import datetime
import pandas as pd

from class_Strategy import Strategy

#td_1y = datetime.timedelta(weeks=52/2)
td_1y = datetime.timedelta(weeks=4)
today = datetime.datetime.now()
start_day = today - td_1y

symbols = 'AAPL'
strategy = Strategy(symbols, start_day, today)
df_bol = strategy.with_moving_ave()
df_RSI = strategy.calcRSI()

c = 10000
NameStrategy = 'BolingerBand'
#NameStrategy = 'RSI'
res = strategy.Backtest(capital = c, name_strategy = NameStrategy)

print('eaning value: ' ,res)
