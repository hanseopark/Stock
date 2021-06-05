import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import datetime

class FinancialStatements:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yfticker = yf.Ticker(ticker)
        self.yfsticker = yfs.get_quote_table(ticker)
        self.yfsBasicStats = yfs.get_stats_valuation(ticker)
        self.yfsAdditionalStats = yfs.get_stats(ticker)
        self.yfssheet = yfs.get_balance_sheet(ticker)
        self.yfsCashFlow = yfs.get_cash_flow(ticker)

    def get_PER(self):
        #pe = yfs.get_quote_table(self.ticker)['PE Ratio (TTM)']
        pe = self.yfsticker['PE Ratio (TTM)']
        return pe

    def get_PBR(self):
        pb = self.yfticker.info['priceToBook']
        return pb

    def get_SECTOR(self):
        info = self.yfticker.info['sector']
        return info

    def get_Beta(self):
        beta = self.yfsticker['Beta (5Y Monthly)']
        return beta

    def get_valuation(self):
        df = self.yfsBasicStats
        df.columns=['Attribute', 'Value']
        df = df[df.Attribute.str.contains("Trailing P/E")]
        df = df.reset_index()
        pe = df.loc[0,'Value']
        return pe


    def get_ROE(self):
        df = self.yfsAdditionalStats
        df.columns=['Attribute', 'Value']
        df = df[df.Attribute.str.contains("Return on Equity")]
        df =df.reset_index()
        roe = df.loc[0,'Value']

        return roe

    def get_ROA(self):
        df = self.yfsAdditionalStats
        df = df[df.Attribute.str.contains("Return on Assets")]
        df =df.reset_index()
        roa = df.loc[0,'Value']
        return roa


    def get_sheet(self):
        df = self.yfssheet
        df = df.loc['totalAssets']
        df = df.reset_index()
        ta = df.loc[0, 'totalAssets']
        return ta

    def get_flow(self):
        pass
        df = self.yfsCashFlow
        return df


