import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs

class FinancialStatements:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yfticker = yf.Ticker(ticker)

    def get_PER(self):
        pe = yfs.get_quote_table(self.ticker)['PE Ratio (TTM)']
        return pe

    def get_PBR(self):
        pb = self.yfticker.info['priceToBook']
        return pb

    def get_SECTOR(self):
        info = self.yfticker.info['sector']
        return info



