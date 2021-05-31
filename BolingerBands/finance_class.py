import pandas as pd
import pandas_datareader as pdr
import datetime

class Stocks:
    def __init__(self, symbol, start_day, end_day):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day

    def get_price_data(self):
        #df_price = pdr.get_data_yahoo(symbol, self.start_day - timedelta(days=365), self.end_day)
        df_price = pdr.DataReader(self.symbol, 'yahoo',self.start_day, self.end_day)

        return df_price

    def with_moving_ave(self):
        df_price = pdr.DataReader(self.symbol, 'yahoo',self.start_day, self.end_day)
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

