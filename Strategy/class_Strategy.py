import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

import json
from tqdm import tqdm
from sklearn.linear_model import LinearRegression

class ShortTermStrategy:

    def __init__(self, symbol, start_day, end_day):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day

    def get_price_data(self):
        df_price = pdr.DataReader(self.symbol, 'yahoo',self. start_day, self.end_day)
        return df_price

    def DayTrading(self, df, df_init, df_end, calendar, capital, day):
        portval = 0
        for date in calendar[::day]:
            prev_date = df_init.index[df_init.index<date][-1]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            prev_value = float(df.loc[prev_date, 'Close'])
            value  = float(df.loc[date, 'Close'])

            dist = (value-prev_value)/value
            if dist >0.025:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value
            #elif dist < -0.015:
            elif dist < -0.05:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value
            else:
                df_end.loc[date, 'Adj Close'] = port_value/df.loc[date, 'Adj Close']
                df_end.loc[date,'cash'] =0

            #print(prev_value, value, dist)
            #print(df.loc[date, 'Adj Close'],df_end.loc[date, 'Adj Close'], port_value)
            portval = port_value

        return portval

    def with_moving_ave(self):
        df_price = pdr.DataReader(self.symbol, 'yahoo',self. start_day, self.end_day)
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

        for i, date in enumerate(pd.to_datetime(df_price.index)):
            temp_df = df_price['Std']
            temp_df = temp_df[:i]
            temp_df = temp_df.dropna()
            mean = temp_df.mean()
            #print(mean)
            df_price.loc[date, 'MeanOfStd'] = mean

        return df_price

    def BolingerBand(self, df, df_init, df_end, calendar, capital):
        std_mean = float(df.loc[:, 'Std'].mean())
        portval = 0
        for date in calendar:
            prev_date = df_init.index[df_init.index<date][-1]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            std = float(df.loc[date, 'Std'])
            #std_mean = float(df.loc[date, 'MeanOfStd'])
            value = float(df.loc[date, 'Adj Close'])
            value_ago = float(df.loc[df_init.index[-4], 'Adj Close'])
            upper = float(df.loc[date, 'bol_upper'])
            if std < std_mean:
                if value > value_ago:
                    if value < upper:
                        df_end.loc[date, 'Adj Close'] = port_value/df.loc[date, 'Adj Close']
                        df_end.loc[date,'cash'] =0
                    else:
                        df_end.loc[date, 'Adj Close'] = 0
                        df_end.loc[date, 'cash'] = port_value
                else:
                    df_end.loc[date, 'Adj Close'] = 0
                    df_end.loc[date, 'cash'] = port_value
            else:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value

            #print(df.loc[date, 'Adj Close'],df_end.loc[date, 'Adj Close'], port_value)
            portval = port_value

        return portval


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

    def RSI(self, df, df_init, df_end, calendar, capital):
        portval = 0
        for date in calendar:
            prev_date = df_init.index[df_init.index<date][-1]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            value = float(df.loc[date, 'RSI'])
            value_signal = float(df.loc[date, 'RSI signal'])

            if value < 40:
                df_end.loc[date, 'Adj Close'] = port_value/df.loc[date, 'Adj Close']
                df_end.loc[date,'cash'] =0
            elif value > 70:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value
            else:
                df_end.loc[date, 'Adj Close'] = df_end.loc[prev_date, 'Adj Close']
                df_end.loc[date, 'cash'] = df_end.loc[prev_date, 'cash']

            #print(value, df.loc[date, 'Adj Close'],df_end.loc[date, 'Adj Close'], df_init.loc[date, 'cash'],port_value)
            portval = port_value

        return portval

    def Backtest(self, capital= 10000, name_strategy='', day = 1):
        pass
        if name_strategy == 'BolingerBand':
            df_origin = self.with_moving_ave()

            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[1:]

            return (self.BolingerBand(df_origin, df_init, df_end, calendar, capital)-capital)/capital*100

        if name_strategy == 'RSI':
            df_origin = self.calcRSI()

            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[1:]

            return (self.RSI(df_origin, df_init, df_end, calendar, capital)-capital)/capital*100

        if name_strategy == 'DayTrading':
            df_origin = self.get_price_data()

            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[1:]

            return (self.DayTrading(df_origin, df_init, df_end, calendar, capital, day)-capital)/capital*100

class LongTermStrategy:
    def __init__(self, url, etf_list, statement):
        url = url+'FS_{0}_{1}.json'.format(etf_list, statement)
        self.url = url

    def get_PER(self):
        df = pd.read_json(self.url)
        df = df[df.Attribute.str.contains("Trailing P/E")]
        df = df.reset_index()
        df_per = df.loc[:,['Ticker','Recent']]
        df_per = df_per.rename(columns = {'Recent': 'PER'})
        df_per.set_index('Ticker', inplace = True)
        df_per['PER'] = df_per['PER'].astype(float)

        return df_per

    def LowPER(self, threshold= 10):
        df = self.get_PER()
        df_per = pd.DataFrame({'PER': []})
        error_symbols = []
        for ticker in tqdm(df.index):
            per = df.loc[ticker, 'PER']
            try:
                if per < threshold:
                    df_per.loc[ticker, 'PER'] = per
            except:
                error_symbols.append(ticker)

        return df_per

    def get_PBR(self):
        df = pd.read_json(self.url)
        df = df[df.Attribute.str.contains("Price/Book")]
        df = df.reset_index()
        df_pbr = df.loc[:,['Ticker','Recent']]
        df_pbr = df_pbr.rename(columns = {'Recent': 'PBR'})
        df_pbr.set_index('Ticker', inplace = True)
        df_pbr['PBR'] = df_pbr['PBR'].astype(float)

        return df_pbr

    def LowPBR(self, threshold=10):
        df = self.get_PBR()
        df = df.sort_values(by='PBR')

        return df

class ToyStrategy:
    def __init__(self):
        pass

class BasicStatement:
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








