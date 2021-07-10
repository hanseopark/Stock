import pandas as pd
import yahoo_fin.stock_info as yfs
from yahoo_fin import news as ynews

import requests
from bs4 import BeautifulSoup

import datetime
from tqdm import tqdm
import json

def main(stock_list, scrap='short'):

    etf_list = yfs.tickers_dow()
    if stock_list == 'dow':
        etf_list = yfs.tickers_dow()
        filename = 'dow'
    elif stock_list == 'sp500':
        filename = 'sp500'
        etf_list = yfs.tickers_sp500()
    elif stock_list == 'nasdaq':
        filename = 'nasdaq'
        etf_list = yfs.tickers_nasdaq()
    elif stock_list == 'other':
        filename = 'other'
        etf_list = yfs.tickers_other()
    elif stock_list == 'selected':
        filename = 'selected'
        url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        etf_list = temp_pd.values.tolist()

    print(etf_list)

    if scrap == 'short':
        error_symbols = []

        total_news_title = {}
        total_news_summary = {}

        for ticker in tqdm(etf_list):
            list_title = []
            list_summary = []
            try:
                list_news= ynews.get_yf_rss(ticker)
                for k,v in enumerate(list_news):
                    list_title.append(v['title'])
                    list_summary.append(v['summary'])

            except:
                error_symbols.append(ticker)
            total_news_title[ticker] = list_title
            total_news_summary[ticker] = list_title

        #print(total_news_title)
        #print(total_news_summary)
        print(error_symbols)

        today = datetime.datetime.now()
        url_title = '/Users/hanseopark/Work/stock/data_news/{0}_{1}_title.json'.format(today.date(), filename)
        url_summary = '/Users/hanseopark/Work/stock/data_news/{0}_{1}_summary.json'.format(today.date(), filename)
        with open (url_title, 'w') as f:
            json.dump(total_news_title, f)

        with open (url_summary, 'w') as f:
            json.dump(total_news_summary, f)

        ## temp reading
#        with open (url, 'r') as f:
#            temp = json.load(f)
#        print(temp)
    elif scrap == 'long':
#       ref: https://zzhu17.medium.com/web-scraping-yahoo-finance-news-a18f9b20ee8a
        url = 'https://news.yahoo.com/dems-head-toward-house-control-160107166.html'
        response = requests.get(url)

        soup = BeautifulSoup(response.text)
        print(soup)

    else:
        print('It is not word correctly')


if __name__ == '__main__':
    s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
    s2 = input('scraping short or long? ')

    print("News' title and summary of stcok in {0} at yahoo finance".format(s))
    main(stock_list=s, scrap=s2)

else:
    pass
