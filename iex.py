import pandas as pd
import pandas_datareader as pdr
import requests
import config

class IEXStocks:

    def __init__ (self, token, symbol):
        #self.BASE_URL = 'https://cloud.iexapis.com/stable/stock'
        self.BASE_URL = 'https://sandbox.iexapis.com/stable/stock'
        self.token = token
        self.symbol = symbol

    def get_logo(self):
        url = f"{self.BASE_URL}/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_company_info(self):
        url = f"{self.BASE_URL}/{self.symbol}/company?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_stats(self):
        url = f"{self.BASE_URL}/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)

        # return r.json()
        return r.text
    def get_chart(self, range):
        self.range = range
        url = f"{self.BASE_URL}/{self.symbol}/chart/{self.range}?token={self.token}"
        r = requests.get(url)
        return r.json()
    # return r.text

    def get_price(self):
        return 0

    def get_news(self, last=10):
        url = f"{self.BASE_URL}/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)

        return r.json()

class YahooStocks:

    def __init__(self, symbol, start_day, end_day):
        self.symbol = symbol
        self.start_day = start_day
        self.end_day = end_day

    def get_price_data(self):
        df_price['SPY'] = pdr.get_data_yahoo('SPY', self.start_day, self.end_day)
        # df_price['SPY'] = df_prcie['Adj Close']
        # df_price = pdr.get_data_yahoo(self.symbol, self.start_day, self.end_day)
        # for ticker in self.symbol:
        # df_price[ticker] = pdr.get_data_yahoo(ticker, self.start_day, self.end_day)
        # df_price[ticker] = pdr.DataReader(ticker, 'yahoo', self.start_day, self.end_day)

        return df_price

    # def get_quote_date(self):
    # 	df = pd.DataFrame(columns=symbol)

    # 	for ticker in self.symbol:
    # 		df[ticker]

    # def get_low_per(self):
