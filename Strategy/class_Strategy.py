import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

import json
from tqdm import tqdm
from pytrends.request import TrendReq
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
        df_price = self.get_price_data()
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
        #std_mean = float(df.loc[:, 'Std'].mean())
        portval = 0
        for date in calendar:
            prev_date = df_init.index[df_init.index<date][-1]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            std = float(df.loc[date, 'Std'])
            std_mean = float(df.loc[date, 'MeanOfStd'])
            value = float(df.loc[date, 'Adj Close'])
            value_ago_ago = float(df.loc[df_init.index[-3], 'Adj Close'])
            value_ago = float(df.loc[df_init.index[-2], 'Adj Close'])
            upper = float(df.loc[date, 'bol_upper'])
            if std < std_mean:
                if value > value_ago and value_ago > value_ago_ago:
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
        df = self.get_price_data()
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
    def __init__(self, url, etfname):
        self.url = url
        self.etfname = etfname

    def get_price_data(self, symbol, OnlyRecent=False):
        self.symbol = symbol
        url_price = self.url+'/FS_'+self.etfname+'_Value.json'
        df = pd.read_json(url_price)

        if OnlyRecent == True:
            temp_df = df[df.Ticker.str.contains(symbol)].copy()
            res = temp_df.loc[temp_df.index[-1], 'Adj Close']

            return res

        return df
#        df_per = df[df.Attribute.str.contains('Trailing P/E')].copy()
#        df_per['PER'] = df_per.loc[:, 'Recent'].astype(float)
#        df_per = df_per.drop(['Attribute', 'Recent'], axis=1)
#        df_per = df_per.set_index('Ticker')


###################################################################################################
    def get_stats(self, preprocessing = False):
        url_stats = self.url+'/FS_'+self.etfname+'_stats.json'
        df = pd.read_json(url_stats)
        if preprocessing == True:
            df_per = self.get_PER() # PER
            df_psr = self.get_PSR() # Price/Sales
            df_pbr = self.get_PBR() # Price/Book
            df_peg = self.get_PEG() # Price/Earning growth
            df_forper = self.get_FORPER() # Forward PER

            # Concat mulit dataframe
            df = pd.concat([df_per, df_psr, df_pbr, df_peg, df_forper], axis=1)

        return df

    def get_addstats(self, preprocessing = False):
        url_addstats = self.url+'/FS_'+self.etfname+'_addstats.json'
        df = pd.read_json(url_addstats)
        if preprocessing == True:
            df_roe = self.get_ROE() # ROE
            df_roa = self.get_ROA() # ROA
            df_pm = self.get_PM() # Profit Margin

            # Concat mulit dataframe
            df = pd.concat([df_roe, df_roa, df_pm], axis=1)

        return df

    def get_balsheets(self, preprocessing = False):
        url_balsheets = self.url+'/FS_'+self.etfname+'_balsheets.json'
        df = pd.read_json(url_balsheets)
        if preprocessing == True:
            df_ta = self.get_TA() # Total Assets

            df = pd.concat([df_ta], axis=1)

        return df

    def get_income(self, preprocessing = False):
        url_income = self.url+'/FS_'+self.etfname+'_income.json'
        df = pd.read_json(url_income)
        if preprocessing == True:
            df_tr = self.get_TR() # Total revenue

            df = pd.concat([df_tr], axis=1)

        return df

    def get_flow(self, preprocessing = False):
        url_flow = self.url+'/FS_'+self.etfname+'_flow.json'
        df = pd.read_json(url_flow)
        if preprocessing == True:
            df_div = self.get_DIV() # Dividends paid across companies
            df_iss = self.get_ISS() # Issuance information

            df = pd.concat([df_div, df_iss], axis=1)

        return df

###################################################################################################
    ## For stats
    def get_stats_element(slef):
        pass
        df = []

        return df
    def get_PER(self):
        df = self.get_stats()
        df_per = df[df.Attribute.str.contains('Trailing P/E')].copy()
        df_per['PER'] = df_per.loc[:, 'Recent'].astype(float)
        df_per = df_per.drop(['Attribute', 'Recent'], axis=1)
        df_per = df_per.set_index('Ticker')

        return df_per

    def get_PSR(self):
        df = self.get_stats()
        df_psr = df[df.Attribute.str.contains('Price/Sales')].copy()
        df_psr['PSR'] = df_psr.loc[:, 'Recent'].astype(float)
        df_psr = df_psr.drop(['Attribute', 'Recent'], axis=1)
        df_psr = df_psr.set_index('Ticker')

        return df_psr

    def get_PBR(self):
        df = self.get_stats()
        df_pbr = df[df.Attribute.str.contains('Price/Book')].copy()
        df_pbr['PBR'] = df_pbr.loc[:, 'Recent'].astype(float)
        df_pbr = df_pbr.drop(['Attribute', 'Recent'], axis=1)
        df_pbr = df_pbr.set_index('Ticker')

        return df_pbr

    def get_PEG(self):
        df = self.get_stats()
        df_peg = df[df.Attribute.str.contains('PEG')].copy()
        df_peg['PEG'] = df_peg.loc[:, 'Recent'].astype(float)
        df_peg = df_peg.drop(['Attribute', 'Recent'], axis=1)
        df_peg = df_peg.set_index('Ticker')

        return df_peg

    def get_FORPER(self):
        df = self.get_stats()
        df_forper = df[df.Attribute.str.contains('Forward P/E')].copy()
        df_forper['forPER'] = df_forper.loc[:, 'Recent'].astype(float)
        df_forper = df_forper.drop(['Attribute', 'Recent'], axis=1)
        df_forper = df_forper.set_index('Ticker')

        return df_forper

    ## For addstats
    def get_ROE(self):
        df = self.get_addstats()
        df_roe = df[df.Attribute.str.contains('Return on Equity')].copy()
        df_roe['ROE'] = df_roe.loc[:, 'Value']
        df_roe = df_roe.drop(['Attribute', 'Value'], axis=1)
        df_roe = df_roe.set_index('Ticker')

        return df_roe

    def get_ROA(self):
        df = self.get_addstats()
        df_roa = df[df.Attribute.str.contains('Return on Assets')].copy()
        df_roa['ROA'] = df_roa.loc[:, 'Value']
        df_roa = df_roa.drop(['Attribute', 'Value'], axis=1)
        df_roa = df_roa.set_index('Ticker')

        return df_roa

    def get_PM(self):
        df = self.get_addstats()
        df_pm = df[df.Attribute.str.contains('Return on Assets')].copy()
        df_pm['ProfitMargin'] = df_pm.loc[:, 'Value']
        df_pm = df_pm.drop(['Attribute', 'Value'], axis=1)
        df_pm = df_pm.set_index('Ticker')

        return df_pm

    ## For balance sheets
    def get_TA(self):
        df = self.get_balsheets()
        df_ta = df[df.Breakdown == 'totalAssets'].copy()
        df_ta['TotalAssets'] = df_ta.loc[:, 'Recent']
        df_ta = df_ta.drop(['Breakdown', 'Recent'], axis=1)
        df_ta = df_ta.set_index('Ticker')

        return df_ta

    ## For Income statements
    def get_TR(self):
        df = self.get_income()
        df_tr = df[df.Breakdown == 'totalRevenue'].copy()
        df_tr['TotalRevenue'] = df_tr.loc[:, 'Recent']
        df_tr = df_tr.drop(['Breakdown', 'Recent'], axis=1)
        df_tr = df_tr.set_index('Ticker')

        return df_tr

    ## For Cash flow
    def get_DIV(self):
        df = self.get_flow()
        df_div = df[df.Breakdown == 'dividendsPaid'].copy()
        df_div['DividendsPaid'] = df_div.loc[:, 'Recent']
        df_div = df_div.drop(['Breakdown', 'Recent'], axis=1)
        df_div = df_div.set_index('Ticker')

        return df_div

    def get_ISS(self):
        df = self.get_flow()
        df_iss = df[df.Breakdown == 'issuanceOfStock'].copy()
        df_iss['Issuance'] = df_iss.loc[:, 'Recent']
        df_iss = df_iss.drop(['Breakdown', 'Recent'], axis=1)
        df_iss = df_iss.set_index('Ticker')

        return df_iss

###################################################################################################
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

    def LowPBR(self, threshold=10):
        df = self.get_PBR()
        df = df.sort_values(by='PBR')
        df = df.head(threshold)

        return df

#    class MLStrategy:
#        def __init__(self, url, etfname):
#            self.url = url
#            self.etfname = etfname


class TrendStrategy:
    def __init__(self, symbol, start_day, end_day, keywords):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day
        self.keywords = keywords

    def get_price_data(self, nomalization = False):
        df_price = pdr.DataReader(self.symbol, 'yahoo',self.start_day, self.end_day)
        if nomalization == True:
            df_price =df_price/df_price.max()
        return df_price

    def get_trend_data(self):
        # it is needed for me to download rating each stock as daily comparing stock's price
        pytrend = TrendReq(hl='en-US', tz=360) # this package is unoffical
        #pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
        #pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',])
        df = pd.DataFrame()
        error_symbol = []
        for ticker in tqdm(self.keywords):
            temp_list = []
            temp_list.append(ticker)
            try:
                pytrend.build_payload(kw_list=temp_list, timeframe='today 12-m')
                df_res = pytrend.interest_over_time()
                df[ticker] = df_res.loc[:, ticker]
                df[ticker] = df[ticker]/df[ticker].max()
            except:
                error_symbol.append(ticker)
        print(error_symbol)
        return df
        #return pytrend


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








