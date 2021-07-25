import numpy as np
import pandas as pd
import pandas_datareader as pdr

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

    def calcRSI(self, symbol, period=14):
        df = self.get_price_data(symbol)
        date_index = df.index.astype('str')
        U = np.where(df.diff(1)['Adj Close'] > 0, df.diff(1)['Adj Close'], 0)
        D = np.where(df.diff(1)['Adj Close'] < 0, df.diff(1)['Adj Close'] * (-1), 0)
        AU = pd.DataFrame(U, index=date_index).rolling(window=period, min_periods=1).mean()
        AD = pd.DataFrame(D, index=date_index).rolling(window=period, min_periods=1).mean()
        RSI = AU/ (AD+AU) * 100

        df.insert(len(df.columns), 'RSI', RSI)
        df.insert(len(df.columns), 'RSI signal', df['RSI'].rolling(window=9, min_periods=1).mean())

        return df
