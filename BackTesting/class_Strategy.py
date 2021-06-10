import numpy as np
import pandas as pd
import pandas_datareader as pdr

class Strategy:

    def __init__(self, symbol, start_day, end_day):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day

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

    def BolingerBand(self, dataframe, dataframe_init, dataframe_end, days, capital):
        df = dataframe
        df_init = dataframe_init
        df_end = dataframe_end
        calendar = days

        std_mean = float(df.loc[:, 'Std'].mean())
        portval = 0
        for date in calendar:
            prev_date = df_init.index[df_init.index<date][-1]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            std = float(df.loc[date, 'Std'])
            #std_mean = float(df.loc[date, 'MeanOfStd'])
            value = float(df.loc[date, 'Adj Close'])
            value_ago = float(df.loc[df.index[-4], 'Adj Close'])
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

    def RSI(self, dataframe, dataframe_init, dataframe_end, days, capital):
        df = dataframe
        df_init = dataframe_init
        df_end = dataframe_end
        calendar = days

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

    def Backtest(self, capital= 10000, name_strategy=''):
        pass
        if name_strategy == 'BolingerBand':
            df_origin = self.with_moving_ave()
            real_val = (df_origin.loc[df_origin.index[-1],'Adj Close'] - df_origin.loc[df_origin.index[0], 'Adj Close'])/df_origin.loc[df_origin.index[-1], 'Adj Close']*100

            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[1:]

            print(real_val)
            return (self.BolingerBand(df_origin, df_init, df_end, calendar, capital)-capital)/capital*100

        if name_strategy == 'RSI':
            df_origin = self.calcRSI()

            real_val = (df_origin.loc[df_origin.index[-1],'Adj Close'] - df_origin.loc[df_origin.index[0], 'Adj Close'])/df_origin.loc[df_origin.index[-1], 'Adj Close']*100
            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[1:]

            print(real_val)
            return (self.RSI(df_origin, df_init, df_end, calendar, capital)-capital)/capital*100













