import pandas as pd
import pandas_datareader as pdr
import datetime

class Stocks:
    def __init__(self, url, filename, start_day, end_day, Offline=False):
        self.url = url
        self.filename = filename
        self.start_day = start_day
        self.end_day = end_day
        self.url_price = self.url+'FS_{}_Value.json'.format(self.filename)
        self.Offline = Offline

    def get_price_data(self, symbol):
        if (self.Offline == True):
            combined_price = pd.read_json(self.url_price)
            df = combined_price[combined_price.Ticker.str.contains(symbol)]
            df_price = df.copy()
            df_price = df_price.set_index('Date')
            df_price = df_price.drop(['Ticker'], axis=1)
            df_price = df_price.loc[df_price.index>=self.start_day]
        else:
            df_price = pdr.DataReader(symbol, 'yahoo', self.start_day, self.end_day)

        return df_price

    def with_moving_ave(self, symbol):
        df_price = self.get_price_data(symbol)
        ma5= df_price['Adj Close'].rolling(window = 5, min_periods=1).mean()
        ma20= df_price['Adj Close'].rolling(window = 20, min_periods=1).mean()
        ma60= df_price['Adj Close'].rolling(window = 60, min_periods=1).mean()
        ma120= df_price['Adj Close'].rolling(window = 120, min_periods=1).mean()
        std = df_price['Adj Close'].rolling(window = 20, min_periods=1).std()
        bol_upper = ma20 + 2*std
        bol_down = ma20 - 2*std

        df_price.insert(len(df_price.columns), 'MA5', ma5)
        df_price.insert(len(df_price.columns), 'MA20', ma20)
        df_price.insert(len(df_price.columns), 'MA60', ma60)
        df_price.insert(len(df_price.columns), 'MA120', ma120)
        df_price.insert(len(df_price.columns), 'Std', std)
        df_price.insert(len(df_price.columns), 'bol_upper', bol_upper)
        df_price.insert(len(df_price.columns), 'bol_down', bol_down)

        return df_price

    def get_price_and_moving_ave(self, value, period):
        pass

