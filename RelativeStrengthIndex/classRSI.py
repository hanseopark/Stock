import numpy as np
import pandas as pd
import pandas_datareader as pdr

class Stocks:
    def __init__(self, symbol, start_day, end_day):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day

    def calcRSI(self, period=14):
        df = pdr.DataReader(self.symbol, 'yahoo',self.start_day, self.end_day)
        date_index = df.index.astype('str')
        U = np.where(df.diff(1)['Adj Close'] > 0, df.diff(1)['Adj Close'], 0)
        D = np.where(df.diff(1)['Adj Close'] < 0, df.diff(1)['Adj Close'] * (-1), 0)
        AU = pd.DataFrame(U, index=date_index).rolling(window=period, min_periods=1).mean()
        AD = pd.DataFrame(D, index=date_index).rolling(window=period, min_periods=1).mean()
        RSI = AU/ (AD+AU) * 100

        df.insert(len(df.columns), 'RSI', RSI)
        df.insert(len(df.columns), 'RSI signal', df['RSI'].rolling(window=9, min_periods=1).mean())

        return df
