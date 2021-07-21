import pandas as pd
import yahoo_fin.stock_info as yfs
from yahoo_fin import news as ynews

import requests
from bs4 import BeautifulSoup

import datetime
from tqdm import tqdm
import json

def main(url = '', index_list = ['AAPL'], index_name = 'dow', scrap='short'):
    url_news = url+'data_news/'

    if scrap == 'short':
        error_symbols = []

        total_news_title = {}
        total_news_summary = {}

        for ticker in tqdm(index_list):
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
        url_title = url_news+'{0}_{1}_title.json'.format(today.date(), index_name)
        url_summary = url_news+'{0}_{1}_summary.json'.format(today.date(), index_name)
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
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")

    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
    elif filename == 'other':
        dow_list = yfs.tickers_other()
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()

    print(dow_list)

    scraping = input('scraping short or long? ')
    print("News' title and summary of stcok in {0} at yahoo finance".format(filename))

    main(url = root_url, index_list = dow_list, index_name=filename, scrap=scraping)

else:
    pass
