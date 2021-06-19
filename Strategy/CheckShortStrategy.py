import datetime
import pandas as pd

from class_Strategy import ShortTermStrategy

#td_1y = datetime.timedelta(weeks=52/2)
td_1y = datetime.timedelta(weeks=52*2)
today = datetime.datetime.now()
start_day = today - td_1y

symbol = input('Write ticker name like aapl: ')
strategy = ShortTermStrategy(symbol, start_day, today)
df_price = strategy.get_price_data()
real_val = (df_price.loc[df_price.index[-1],'Adj Close'] - df_price.loc[df_price.index[0], 'Adj Close'])/df_price.loc[df_price.index[-1], 'Adj Close']*100

c = 10000
list_strategy = ['BolingerBand', 'RSI', 'DayTrading', 'WeekTrading']
for s in list_strategy:
    NameStrategy = s
    res = strategy.Backtest(capital = c, name_strategy = NameStrategy)

    print('*'*100)
    print('{}'.format(s))
    print('Real val: ', real_val)
    print('eaning value: ' ,res)
print('*'*100)
