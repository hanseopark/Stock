## ONLINE TESTING ##

import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

import math
import datetime

class FinancialStatements:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yfticker = yf.Ticker(ticker)
        self.yfsquote = yfs.get_quote_table(ticker)
        self.yfsticker = yfs.get_quote_table(ticker)
        self.yfsBasicStats = yfs.get_stats_valuation(ticker)
        self.yfsAdditionalStats = yfs.get_stats(ticker)
        self.yfsSheet = yfs.get_balance_sheet(ticker)
        self.yfsCashFlow = yfs.get_cash_flow(ticker)

    def print_quote(self):
        print(self.yfsquote)

    def get_Basic(self):
        return self.yfsBasicStats

    def print_Basic(self):
        print(self.yfsBasicStats)

    def get_Add(self):
        return self.yfsAdditionalStats

    def print_Add(self):
        print(self.yfsAdditionalStats)

    def get_Sheet(self):
        return self.yfsSheet

    def print_Sheet(self):
        print(self.yfsSheet)

    def get_CashFlow(self):
        return self.yfsCashFlow

    def print_Basic(self):
        print(self.yfsBasicStats)

    def print_Add(self):
        print(self.yfsAdditionalStats)

    def print_Sheet(self):
        print(self.yfsSheet)

    def print_CashFlow(self):
        print(self.yfsCashFlow)

    def get_PER(self):
        #pe = yfs.get_quote_table(self.ticker)['PE Ratio (TTM)']
        pe = self.yfsquote['PE Ratio (TTM)']
        return pe

    def get_PBR(self):
        pb = self.yfticker.info['priceToBook']
        return pb

    def get_SECTOR(self):
        info = self.yfticker.info['sector']
        return info

    def get_Beta(self):
        beta = self.yfsquote['Beta (5Y Monthly)']
        return beta

    def get_valuation(self):
        df = self.yfsBasicStats
        df.columns=['Attribute', 'Value']
        df = df[df.Attribute.str.contains("Trailing P/E")]
        df = df.reset_index()
        pe = df.loc[0,'Value']
        return pe

    def get_NetProfit(self):
        df = self.yfsAdditionalStats
        df = df[df.Attribute.str.contains("Net Income")]
        df = df.reset_index()
        np = df.loc[0,'Value']

        return np

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
        roa = float(roa[:-1])
        return roa


    def get_totalAssets(self):
        list_ta = []
        df = self.yfsSheet
        df = df.loc['totalAssets']
        df = df.reset_index()
        list_ta = df['totalAssets'].to_list()
        return list_ta

    def get_LEV(self):
        list_debt = []
        list_LEV = []
        df = self.yfsAdditionalStats
        df = df.loc['longTermDebt']
        df = df.reset_index()
        list_debt = df['longTermDebt'].to_list()
        for i in range (len(list_debt)):
            list_LEV = list_debt[i]/self.get_totalAssets[i]
        return list_LEV

    def get_LIQ(self):
        list_ca = []
        list_cl = []
        df = self.yfsAdditionalStats
        df_ca = df.loc['totalCurrentAssets']
        df_ca = df_ca.reset_index()
        list_ca = df_ca['totalCurrentAssets'].to_list()
        df_cl = df.loc['totalCurrentLiabilities']
        df_cl = df_cl.reset_index()
        list_cl = df_cl['totalCurrentLiabilities'].to_list()
        list_liq = []
        for i in range(len(list_ca)):
            list_liq = list_ca[i]/list_cl[i]
        return list_liq

    def get_OFFER(self):
        list_ics = []
        df = self.yfsCashFlow
        df = df.loc['issuanceOfStock']
        df = df.reset_index()
        list_ics = df['issuanceOfStock'].to_list()
        return list_ics

    def get_ProfitMargin(self):
        df = self.yfsAdditionalStats
        df = df[df.Attribute.str.contains("Profit Margin")]
        df =df.reset_index()
        pm = df.loc[0,'Value']
        pm = float(pm[:-1])
        return pm

    def get_OperatingMargin(self):
        df = self.yfsAdditionalStats
        df = df[df.Attribute.str.contains("Profit Margin")]
        df =df.reset_index()
        om = df.loc[0,'Value']
        om = float(om[:-1])
        return om

    def get_cashflow(self):
        pass
        list_cf = [0.0, 0.0]
        df = self.yfsAdditionalStats
        df = df[df.Attribute.str.contains("Operating Cash Flow")]
        df =df.reset_index()
        cf = df.loc[0,'Value']
        cf = float(cf[:-1])
        cf = cf*pow(10,9)
        return cf
#        list_cf[0] = cf
#
#        df = self.yfsCashFlow
#        #df2 = df2[df2.Attribute.str.contains('totalCashFromOperatingActivities')]
#        df = df.loc['totalCashFromOperatingActivities']
#        df = df.reset_index()
#        cf = df.loc[0,'totalCashFromOperatingActivities']
#        list_cf[1] = cf
#
#        return list_cf

    def get_CFO(self):
        pass
        #return self.get_cashflow()/self.get_totalAssets()
        return self.yfsAdditionalStats
        return 0

    def get_FScore(self):
        ROA = self.get_ROA()
        CFO = self.get_CFO()
