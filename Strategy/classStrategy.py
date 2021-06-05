import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import datetime
from sklearn.linear_model import LinearRegression

class BasicStrategy:
    def __init__(self, ticker, start_day, end_day):
        self.ticker = ticker
        self.start_day = start_day
        self.end_day = end_day
        self.yfticker = yf.Ticker(ticker)

    def Calculate_Beta(self):
        symbol_list = [self.ticker,'SPY']
        df = yf.download(symbol_list, self.start_day)['Adj Close']
        price_change = df.pct_change()
        df_ForBeta = price_change.drop(price_change.index[0])
        x = np.array(df_ForBeta['SPY']).reshape([-1,1])
        y = np.array(df_ForBeta[self.ticker])
        model = LinearRegression().fit(x, y)

        return model.coef_


class AdvancedStratedy:
    pass



