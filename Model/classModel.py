import pandas as pd
import numpy as np
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs
import datetime

def daterange(start_date, end_date, step):
    end_date = end_date-5*datetime.timedelta(step)
    for n in range(0, int((end_date-start_date).days) +1, step):
        yield start_date+datetime.timedelta(n)

class priceModel:
    def __init__(self, url, filename, start_day, end_day, Offline=False, run_yfs=False):
        self.url = url
        self.filename = filename
        self.start_day = start_day
        self.end_day = end_day
        self.url_price = self.url+'FS_{}_Value.json'.format(self.filename)
        self.Offline = Offline
        self.run_yfs = run_yfs

    def get_price_data(self, symbol):
        if (self.Offline == True):
            combined_price = pd.read_json(self.url_price)
            df = combined_price[combined_price.Ticker.str.contains(symbol)]
            df_price = df.copy()
            df_price = df_price.set_index('Date')
            df_price = df_price.drop(['Ticker'], axis=1)
            df_price = df_price.loc[df_price.index>=self.start_day]
        else:
            if self.run_yfs==False:
                df_price = pdr.DataReader(symbol, 'yahoo', self.start_day, self.end_day)
            else:
                self.start_day.strftime('%m/%d/%y')
                self.end_day.strftime('%m/%d/%y')
                df_price = yfs.get_data(symbol, start_date=self.start_day, end_date = self.end_day)
                df_price = df_price.rename(columns={'open':'Open', 'index':'Date', 'high':'High','low':'Low','close':'Close','adjclose':'Adj Close','volume':'Volume','ticker':'Ticker'})
                df_price = df_price[['Ticker','High','Low','Open','Close','Volume','Adj Close']]
                df_price = df_price.drop(['Ticker'], axis=1)

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

    def JudgeMarket(self, symbol):
        df = self.with_moving_ave(symbol)
        df['JudgeMA5'] = np.where(df['Adj Close'] > df['MA5'], 'BullMarket', 'BearMarket')
        df['JudgeMA20'] = np.where(df['Adj Close'] > df['MA20'], 'BullMarket', 'BearMarket')
        df['JudgeMA60'] = np.where(df['Adj Close'] > df['MA60'], 'BullMarket', 'BearMarket')
        df['JudgeMA120'] = np.where(df['Adj Close'] > df['MA120'], 'BullMarket', 'BearMarket')

        return df

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

class FSModel:
    def __init__(self, url, filename, Offline=False):
        self.url = url
        self.filename = filename

        self.url_stats = self.url+'FS_{}_stats.json'.format(self.filename)
        self.url_addstats = self.url+'FS_{}_addstats.json'.format(self.filename)
        self.url_balsheets = self.url+'FS_{}_balsheets.json'.format(self.filename)
        self.url_income = self.url+'FS_{}_income.json'.format(self.filename)
        self.url_flow = self.url+'FS_{}_flow.json'.format(self.filename)

        self.Offline = Offline

    def getStats(self, symbol):
        if self.Offline==True:
            combined_addstats = pd.read_json(self.url_stats)
            df = combined_addstats[combined_addstats.Ticker.str.contains(symbol)]
        else:
            df = yfs.get_stats_valuation(symbol)
            df =df.iloc[:,:2]
            df.columns = ['Attribute', 'Recent']

        return df

    def getAddstats(self, symbol):
        if self.Offline==True:
            combined_addstats = pd.read_json(self.url_addstats)
            df = combined_addstats[combined_addstats.Ticker.str.contains(symbol)]
        else:
            df = yfs.get_stats(symbol)
        return df

##### For model high #####
    def getHigh(self, symbol):
        df = self.getAddstats(symbol)
        if self.Offline==True:
            df_high = df[df.Attribute.str.contains('High')].copy()
            df_high = df_high.drop(['Ticker'],axis=1)
            high = df_high['Value'].item()
        else:
            df_high = df[df.Attribute.str.contains('High')].copy()
            high = df_high['Value'].item()

        return high

##### For checking safety #####
    def getCap(self, symbol):
        df = self.getStats(symbol)
        df_cap = df[df.Attribute.str.contains('Cap')].copy()
        if self.Offline==True:
            df_cap = df_cap.drop(['Ticker'],axis=1)
            cap = df_cap['Value'].item()
        else:
            cap = df_cap['Recent'].item()

        return cap

    def getPER(self, symbol):
        df = self.getStats(symbol)
        df_forper = df[df.Attribute.str.contains('Forward P/E')].copy()
        if self.Offline==True:
            df_forper['forPER'] = df_forper.loc[:, 'Recent']
            df_forper = df_forper.drop(['Attribute', 'Recent'], axis=1)
        else:
            per = df_forper['Recent'].item()

        return per

class Wallet:
    def __init__(self, capital = 10000):
        self.capital = capital

    def EarningValue(self, tickers, period=5):
        pass
