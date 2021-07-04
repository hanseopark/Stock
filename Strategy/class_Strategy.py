import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs
from yahoo_fin import news as ynews

import json
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
from pytrends.request import TrendReq
from pytrends import dailydata
from sklearn.linear_model import LinearRegression

class ShortTermStrategy:

    def __init__(self, symbol, start_day, end_day, url = '', Offline=False):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day
        self.url = url
        self.Offline = Offline

    def get_price_data(self):
        if (self.Offline == True):
            url_price = self.url+'/FS_{0}_Value.json'.format('sp500') # If you have nasdaq stocks, you'd like to choose nasdaq stocks rather than sp500 or dow to have many data sets
            combined_price = pd.read_json(url_price)
            df = combined_price[combined_price.Ticker.str.contains(self.symbol)]
            df_price = df.copy()
            df_price = df_price.set_index('Date')
            df_price = df_price.drop(['Ticker'], axis=1)
            df_price = df_price.loc[self.start_day : self.end_day]

        else:
            df_price = pdr.DataReader(self.symbol, 'yahoo',self.start_day, self.end_day)

        return df_price

    def DayTrading(self, df, df_init, df_end, calendar, capital, day, upper_limit = 0.025, down_limit= -0.05):
        portval = 0
        for date in calendar[::day]:
            prev_date = df_init.index[df_init.index<date][-day]
            df_init.loc[date, :] = df_end.loc[prev_date, :]
            port_value = df_init.loc[date, 'Adj Close'] * df.loc[date, 'Adj Close'] + df_init.loc[date, 'cash']

            prev_value = float(df.loc[prev_date, 'Close'])
            value  = float(df.loc[date, 'Close'])

            disc = (value-prev_value)/value
            if disc >upper_limit:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value
            elif disc < down_limit:
                df_end.loc[date, 'Adj Close'] = 0
                df_end.loc[date, 'cash'] = port_value
            else:
                df_end.loc[date, 'Adj Close'] = port_value/df.loc[date, 'Adj Close']
                df_end.loc[date,'cash'] =0

            #print(prev_value, value, disc)
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

    def Backtest(self, capital= 10000, name_strategy=''):
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

        if name_strategy == 'DayTrading' or name_strategy == 'WeekTrading':
            if name_strategy == 'DayTrading':
                days_step = 1
            elif name_strategy == 'WeekTrading':
                days_step = 5
            df_origin = self.get_price_data()

            df_init = (df_origin*0).assign(cash = 0)
            df_end = (df_origin*0).assign(cash = 0)

            df_init.iloc[0, df_init.columns.get_loc('cash')] = capital
            df_end.iloc[0, df_end.columns.get_loc('cash')] = capital

            calendar = pd.Series(df_origin.index).iloc[days_step:]

            return (self.DayTrading(df_origin, df_init, df_end, calendar, capital, day=days_step)-capital)/capital*100

        return 0

class LongTermStrategy:
    def __init__(self, url, etfname, Offline = False):
        self.url = url
        self.etfname = etfname
        self.Offline = Offline

    def get_ticker_list(self):
        df = self.get_stats()
        list_ticker = sorted(list(set(df['Ticker'].to_list())))

        return list_ticker

    def get_price_data(self, etf_list=[], OnlyRecent=False):
        self.etf_list = etf_list
        url_price = self.url+'/data_origin/FS_'+self.etfname+'_Value.json'
        combined_price = pd.read_json(url_price)
        df_price = pd.DataFrame({'Recent_price': []})

        if OnlyRecent == True:
            if self.Offline == True:
                print('Recent price by offline datasets')
                for symbol in tqdm(self.etf_list):
                    temp_df = combined_price[combined_price.Ticker.str.contains(symbol)].copy()
                    res = temp_df.loc[temp_df.index[-1], 'Adj Close']
                    df_price.loc[symbol, 'Recent_price'] =res
                return df_price

            else:
                print('LIVE Recent price')
                for symbol in tqdm(self.etf_list):
                    df_price.loc[symbol, 'Recent_price'] = yfs.get_live_price(symbol)
                return df_price

        else:
            df_price = combined_price.copy()
            return df_price

###################################################################################################
    def get_stats(self, preprocessing = False):
        url_stats = self.url+'/data_origin/FS_'+self.etfname+'_stats.json'
        df = pd.read_json(url_stats)
        if preprocessing == True:
            df_per = self.get_PER() # PER
            df_psr = self.get_PSR() # Price/Sales
            df_pbr = self.get_PBR() # Price/Book
            df_peg = self.get_PEG() # Price/Earning growth
            df_forper = self.get_FORPER() # Forward PER
            df_cap = self.get_CAP() # Market Cap

            # Concat mulit dataframe
            df = pd.concat([df_per, df_psr, df_pbr, df_peg, df_forper, df_cap], axis=1)

        return df

    def get_addstats(self, preprocessing = False):
        url_addstats = self.url+'/data_origin/FS_'+self.etfname+'_addstats.json'
        df = pd.read_json(url_addstats)
        if preprocessing == True:
            df_beta = self.get_Beta()
            df_divr = self.get_DivRate() # Annual diviend rate
            df_roe = self.get_ROE() # ROE
            df_roa = self.get_ROA() # ROA
            df_pm = self.get_PM() # Profit Margin
            df_cash = self.get_Cash() # Total Cash
            df_debt = self.get_Debt() # Total Debt

            # Concat mulit dataframe
            df = pd.concat([df_beta, df_divr, df_roe, df_roa, df_pm, df_cash, df_debt], axis=1)

        return df

    def get_balsheets(self, preprocessing = False):
        url_balsheets = self.url+'/data_origin/FS_'+self.etfname+'_balsheets.json'
        df = pd.read_json(url_balsheets)
        if preprocessing == True:
            df_ta = self.get_TA() # Total Assets

            df = pd.concat([df_ta], axis=1)

        return df

    def get_income(self, preprocessing = False):
        url_income = self.url+'/data_origin/FS_'+self.etfname+'_income.json'
        df = pd.read_json(url_income)
        if preprocessing == True:
            df_tr = self.get_TR() # Total revenue

            df = pd.concat([df_tr], axis=1)

        return df

    def get_flow(self, preprocessing = False):
        url_flow = self.url+'/data_origin/FS_'+self.etfname+'_flow.json'
        df = pd.read_json(url_flow)
        if preprocessing == True:
            df_div = self.get_DIV() # Dividends paid across companies
            df_iss = self.get_ISS() # Issuance information

            df = pd.concat([df_div, df_iss], axis=1)

        return df

###################################################################################################
## For stats
def get_stats_element(self, etf_list =['AAPL']):
        df_stats = self.get_stats()
        self.etf_list = etf_list
        temp_df = df_stats[df_stats.Ticker == etf_list[0]].copy()
        list_df = temp_df['Attribute'].to_list()
        df = pd.DataFrame(columns=list_df, index = self.etf_list)
        print('For stats')
        for ticker in tqdm(self.etf_list):
            temp_df = df_stats[df_stats.Ticker == ticker].copy()
            list_df = temp_df['Attribute'].to_list()
            for att in list_df:
                temp_df_stats = df_stats[df_stats.Attribute == att].copy()
                temp_df_stats = temp_df_stats.set_index('Ticker')
                df.loc[ticker, att] = temp_df_stats.loc[ticker, 'Recent']

        url_stats = self.url+'/data_preprocessing/'+self.etfname+'_stasts_element'
        df.astype(float).to_json(url_stats+'.json')
        df.astype(float).to_csv(url_stats+'.csv')

        return df

    def get_PER(self):
        df = self.get_stats()
        df_per = df[df.Attribute.str.contains('Trailing P/E')].copy()
        df_per['PER'] = df_per.loc[:, 'Recent']
        df_per = df_per.drop(['Attribute', 'Recent'], axis=1)
        df_per = df_per.set_index('Ticker')
        df_per = df_per.fillna(value=np.nan)
        df_temp = pd.DataFrame()
        for col in df_per.columns:
            df_temp[col] = pd.to_numeric(df_per[col], errors='coerce')

        return df_temp.astype(float)


        #return df_per.astype(float)

    def get_PSR(self):
        df = self.get_stats()
        df_psr = df[df.Attribute.str.contains('Price/Sales')].copy()
        df_psr['PSR'] = df_psr.loc[:, 'Recent']
        df_psr = df_psr.drop(['Attribute', 'Recent'], axis=1)
        df_psr = df_psr.set_index('Ticker')
        df_psr = df_psr.fillna(value=np.nan)
        df_temp = pd.DataFrame()
        for col in df_psr.columns:
            df_temp[col] = pd.to_numeric(df_psr[col], errors='coerce')

        return df_temp.astype(float)

    def get_PBR(self):
        df = self.get_stats()
        df_pbr = df[df.Attribute.str.contains('Price/Book')].copy()
        df_pbr['PBR'] = df_pbr.loc[:, 'Recent']
        df_pbr = df_pbr.drop(['Attribute', 'Recent'], axis=1)
        df_pbr = df_pbr.set_index('Ticker')

        return df_pbr.astype(float)

    def get_PEG(self):
        df = self.get_stats()
        df_peg = df[df.Attribute.str.contains('PEG')].copy()
        df_peg['PEG'] = df_peg.loc[:, 'Recent']
        df_peg = df_peg.drop(['Attribute', 'Recent'], axis=1)
        df_peg = df_peg.set_index('Ticker')

        return df_peg.astype(float)

    def get_FORPER(self):
        df = self.get_stats()
        df_forper = df[df.Attribute.str.contains('Forward P/E')].copy()
        df_forper['forPER'] = df_forper.loc[:, 'Recent']
        df_forper = df_forper.drop(['Attribute', 'Recent'], axis=1)
        df_forper = df_forper.set_index('Ticker')
        df_forper = df_forper.fillna(value=np.nan)
        df_temp = pd.DataFrame()
        for col in df_forper.columns:
            df_temp[col] = pd.to_numeric(df_forper[col], errors='coerce')

        return df_temp

    def get_CAP(self):
        df = self.get_stats()
        df_cap = df[df.Attribute.str.contains('Cap')].copy()
        df_cap['marketCap'] = df_cap.loc[:, 'Recent']
        df_cap = df_cap.drop(['Attribute', 'Recent'], axis=1)
        df_cap = df_cap.set_index('Ticker')
        df_cap = df_cap.fillna(value=np.nan)
        for ticker in df_cap.index:
            value = df_cap.loc[ticker, 'marketCap']
            if type(value) == str:
                value = float(value.replace('.','').replace('T','0000000000').replace('B','0000000').replace('M','0000').replace('k','0'))
            df_cap.loc[ticker, 'marketCap'] = value

        return df_cap.astype(float)


    ## For addstats
    def get_addstats_element(self, etf_list =['AAPL']):
        df_stats = self.get_addstats()
        self.etf_list = etf_list
        temp_df = df_stats[df_stats.Ticker == etf_list[0]].copy()
        list_df = temp_df['Attribute'].to_list()
        df = pd.DataFrame(columns=list_df, index = self.etf_list)
        print('For addstats')
        for ticker in tqdm(self.etf_list):
            temp_df = df_stats[df_stats.Ticker == ticker].copy()
            list_df = temp_df['Attribute'].to_list()
            for att in list_df:
                temp_df_stats = df_stats[df_stats.Attribute == att].copy()
                temp_df_stats = temp_df_stats.set_index('Ticker')
                df.loc[ticker, att] = temp_df_stats.loc[ticker, 'Value']

        url_stats = self.url+'/data_preprocessing/'+self.etfname+'_addstatsa_element'
        df.astype(float).to_json(url_stats+'.json')
        df.astype(float).to_csv(url_stats+'.csv')

        return df

    def get_Beta(self):
        df = self.get_addstats()
        df_beta = df[df.Attribute.str.contains('Beta')].copy()
        df_beta['Beta'] = df_beta.loc[:, 'Value']
        df_beta = df_beta.drop(['Attribute', 'Value'], axis=1)
        df_beta = df_beta.set_index('Ticker')

        #return df_beta.astype(float)
        return df_beta.astype(float)

    def get_DivRate(self):
        df = self.get_addstats()
        df_divr = df[df.Attribute.str.contains('Trailing Annual Dividend Rate')].copy()
        df_divr['AnnualDividendRate']= df_divr.loc[:, 'Value']
        df_divr = df_divr.drop(['Attribute', 'Value'], axis=1)
        df_divr = df_divr.set_index('Ticker')

        #return df_divr.astype(float)
        return df_divr.astype(float)

    def get_ROE(self):
        df = self.get_addstats()
        df_roe = df[df.Attribute.str.contains('Return on Equity')].copy()
        df_roe['ROE(%)'] = df_roe.loc[:, 'Value']
        df_roe = df_roe.drop(['Attribute', 'Value'], axis=1)
        df_roe = df_roe.set_index('Ticker')
        df_roe = df_roe.fillna(value=np.nan)
        for ticker in df_roe.index:
            value = df_roe.loc[ticker, 'ROE(%)']
            if type(value) == str:
                value = float(value[:-1].replace(',',''))
            df_roe.loc[ticker, 'ROE(%)'] = value

        return df_roe.astype(float)

    def get_ROA(self):
        df = self.get_addstats()
        df_roa = df[df.Attribute.str.contains('Return on Assets')].copy()
        df_roa['ROA(%)'] = df_roa.loc[:, 'Value']
        df_roa = df_roa.drop(['Attribute', 'Value'], axis=1)
        df_roa = df_roa.set_index('Ticker')
        df_roa = df_roa.fillna(value=np.nan)
        for ticker in df_roa.index:
            value = df_roa.loc[ticker, 'ROA(%)']
            if type(value) == str:
                value = float(value[:-1].replace(',',''))
            df_roa.loc[ticker, 'ROA(%)'] = value

        return df_roa.astype(float)

    def get_PM(self):
        df = self.get_addstats()
        df_pm = df[df.Attribute.str.contains('Profit Margin')].copy()
        df_pm['ProfitMargin(%)'] = df_pm.loc[:, 'Value']
        df_pm = df_pm.drop(['Attribute', 'Value'], axis=1)
        df_pm = df_pm.set_index('Ticker')
        df_pm = df_pm.fillna(value=np.nan)
        for ticker in df_pm.index:
            value = df_pm.loc[ticker, 'ProfitMargin(%)']
            if type(value) == str:
                value = float(value[:-1].replace(',',''))
            df_pm.loc[ticker, 'ProfitMargin(%)'] = value

        return df_pm.astype(float)

    def get_Cash(self):
        df = self.get_addstats()
        df_cash = df[df.Attribute.str.contains('Total Cash Per Share')].copy()
        df_cash['TotalCash'] = df_cash.loc[:, 'Value']
        df_cash = df_cash.drop(['Attribute', 'Value'], axis=1)
        df_cash = df_cash.set_index('Ticker')

        return df_cash.astype(float)

    def get_Debt(self):
        df = self.get_addstats()
        df_debt = df[df.Attribute.str.contains('Total Debt/Equity')].copy()
        df_debt['TotalDebt'] = df_debt.loc[:, 'Value']
        df_debt = df_debt.drop(['Attribute', 'Value'], axis=1)
        df_debt = df_debt.set_index('Ticker')

        return df_debt.astype(float)

    ## For balance sheets

    def get_balsheets_element(self, etf_list =['AAPL']):
        df_stats = self.get_balsheets()
        self.etf_list = etf_list
        temp_df = df_stats[df_stats.Ticker == etf_list[0]].copy()
        list_df = temp_df['Breakdown'].to_list()
        df = pd.DataFrame(columns=list_df, index = self.etf_list)
        print('For balance sheets')
        for ticker in tqdm(self.etf_list):
            temp_df = df_stats[df_stats.Ticker == ticker].copy()
            list_df = temp_df['Breakdown'].to_list()
            for att in list_df:
                temp_df_stats = df_stats[df_stats.Breakdown == att].copy()
                temp_df_stats = temp_df_stats.set_index('Ticker')
                df.loc[ticker, att] = temp_df_stats.loc[ticker, 'Recent']
        url_stats = self.url+'/data_preprocessing/'+self.etfname+'_balsheets_element'
        df.astype(float).to_json(url_stats+'.json')
        df.astype(float).to_csv(url_stats+'.csv')

        return df.astype(float)

    def get_TA(self):
        df = self.get_balsheets()
        df_ta = df[df.Breakdown == 'totalAssets'].copy()
        df_ta['TotalAssets'] = df_ta.loc[:, 'Recent']
        df_ta = df_ta.drop(['Breakdown', 'Recent'], axis=1)
        df_ta = df_ta.set_index('Ticker')

        return df_ta

    ## For Income statements

    def get_income_element(self, etf_list =['AAPL']):
        df_stats = self.get_income()
        self.etf_list = etf_list
        temp_df = df_stats[df_stats.Ticker == etf_list[0]].copy()
        list_df = temp_df['Breakdown'].to_list()
        df = pd.DataFrame(columns=list_df, index = self.etf_list)
        print('For income statements')
        error_symbols = []
        for ticker in tqdm(self.etf_list):
            temp_df = df_stats[df_stats.Ticker == ticker].copy()
            list_df = temp_df['Breakdown'].to_list()
            for att in list_df:
                temp_df_stats = df_stats[df_stats.Breakdown == att].copy()
                temp_df_stats = temp_df_stats.set_index('Ticker')
                df.loc[ticker, att] = temp_df_stats.loc[ticker, 'Recent']
            error_symbols.append(ticker)

        print('Error symbol: ', error_symbols)
        url_stats = self.url+'/data_preprocessing/'+self.etfname+'_income_element'
        df.astype(float).to_json(url_stats+'.json')
        df.astype(float).to_csv(url_stats+'.csv')

        return df.astype(float)

    def get_TR(self):
        df = self.get_income()
        df_tr = df[df.Breakdown == 'totalRevenue'].copy()
        df_tr['TotalRevenue'] = df_tr.loc[:, 'Recent']
        df_tr = df_tr.drop(['Breakdown', 'Recent'], axis=1)
        df_tr = df_tr.set_index('Ticker')

        return df_tr

    ## For Cash flow

    def get_flow_element(self, etf_list =['AAPL']):
        df_stats = self.get_flow()
        self.etf_list = etf_list
        temp_df = df_stats[df_stats.Ticker == etf_list[0]].copy()
        list_df = temp_df['Breakdown'].to_list()
        df = pd.DataFrame(columns=list_df, index = self.etf_list)
        print('For cash flow')
        for ticker in tqdm(self.etf_list):
            temp_df = df_stats[df_stats.Ticker == ticker].copy()
            list_df = temp_df['Breakdown'].to_list()
            for att in list_df:
                temp_df_stats = df_stats[df_stats.Breakdown == att].copy()
                temp_df_stats = temp_df_stats.set_index('Ticker')
                df.loc[ticker, att] = temp_df_stats.loc[ticker, 'Recent']
        url_stats = self.url+'/data_preprocessing/'+self.etfname+'_flow_element'
        df.astype(float).to_json(url_stats+'.json')
        df.astype(float).to_csv(url_stats+'.csv')

        return df.astype(float)

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
    def __init__(self, symbol, index, start, end, keywords):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.keywords = keywords
        self.index = index

    def get_price_data(self, nomalization = False, DoSymbol = False):
        if DoSymbol == True:
            df_price = pdr.DataReader(self.symbol, 'yahoo',self.start, self.end)
            if nomalization == True:
                df_price['Adj Close'] =df_price['Adj Close']/df_price['Adj Close'].max()
            return df_price['Adj Close']
        else:
            df_price = pdr.DataReader(self.index, 'yahoo',self.start, self.end)
            if nomalization == True:
                df_price =df_price/df_price.max()
            return df_price

    def get_trend_data(self, DoSymbol = False):
        # it is needed for me to download rating each stock as daily comparing stock's price
        if DoSymbol == True:
            list_temp = [self.symbol]
            pytrend = TrendReq(hl='en-US', tz=360) # this package is unoffical
            #pytrend.build_payload(kw_list=list_temp, timeframe='today 12-m')

            #df = pytrend.interest_over_time()
            df = dailydata.get_daily_data(self.symbol, int(self.start.year), int(self.start.month), int(self.end.year), int(self.end.month))

            df[self.symbol] = df[self.symbol]/df[self.symbol].max()

            return df[self.symbol]

        else:
            pytrend = TrendReq(hl='en-US', tz=360) # this package is unoffical
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
            return df

class NLPStrategy:
    def __init__(self, url, etfname, Offline = False):
        self.url = url
        self.etfname = etfname
        self.Offline = Offline

    def get_news_title(self, ticker = 'AAPL'):
        if self.Offline == True:
            url_news = self.url+'/data_origin/FS_'+self.etfname+'_title.json'
            with open (url_news, 'r') as f:
                title = json.load(f)
        else:
            title = []
            news = ynews.get_yf_rss(ticker)
            for k,v in enumerate(news):
                title.append(v['title'])

        return title

    def get_news_summary(self, ticker = 'AAPL'):
        if self.Offline == True:
            url_news = self.url+'/data_origin/FS_'+self.etfname+'_summary.json'
            with open (url_news, 'r') as f:
                title = json.load(f)
        else:
            summary = []
            news = ynews.get_yf_rss(ticker)
            for k,v in enumerate(news):
                summary.append(v['summary'])

        return summary

class BasicStatement:
    def __init__(self, ticker, start_day, end_day):
        self.ticker = ticker
        self.start_day = start_day
        self.end_day = end_day
        self.yfticker = yf.Ticker(ticker)

    def Calculate_Beta(self):
        symbol_list = [self.ticker,'^IXIC']
        df = yf.download(symbol_list, self.start_day)['Adj Close']
        price_change = df.pct_change()
        df_ForBeta = price_change.drop(price_change.index[0])
        x = np.array(df_ForBeta['^IXIC']).reshape([-1,1])
        y = np.array(df_ForBeta[self.ticker])
        model = LinearRegression().fit(x, y)

        return model.coef_

class AdvancedStratedy:
    pass
