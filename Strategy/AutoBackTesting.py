import datetime
import pandas as pd

from class_Strategy import ShortTermStrategy

td_1y = datetime.timedelta(weeks=52)
#td_1y = datetime.timedelta(weeks=4)
today = datetime.datetime.now()
start_day = today - td_1y

url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
temp_pd = pd.read_json(url)
temp_pd = temp_pd['Ticker']
dow_list = temp_pd.values.tolist()

for ticker in dow_list:
    print('*'*100)
    print('*'*45,' ',ticker ,' ', '*'*46)
    print('*'*100)
    strategy = ShortTermStrategy(ticker, start_day, today)
    df_price = strategy.get_price_data()
    real_val = (df_price.loc[df_price.index[-1],'Adj Close'] - df_price.loc[df_price.index[0], 'Adj Close'])/df_price.loc[df_price.index[-1], 'Adj Close']*100

    c = 10000
    list_strategy = ['BolingerBand', 'RSI', 'DayTrading']
    for s in list_strategy:
        NameStrategy = s
        res = strategy.Backtest(capital = c, name_strategy = NameStrategy, day=1)

        print('*'*100)
        print('{}'.format(s))
        print('Real val: ', real_val)
        print('eaning value: ' ,res)
    print('*'*100)
