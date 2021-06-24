import json
import pandas as pd
import yahoo_fin.stock_info as yfs
from yahoo_fin import news as ynews

from tqdm import tqdm

def main(stock_list):

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

    url_title = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_title.json'.format(filename)
    url_summary = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_summary.json'.format(filename)
    with open (url_title, 'w') as f:
        json.dump(total_news_title, f)

    with open (url_summary, 'w') as f:
        json.dump(total_news_summary, f)

    ## temp reading
#    with open (url, 'r') as f:
#        temp = json.load(f)
#    print(temp)

if __name__ == '__main__':
    s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")

    print("News' title and summary of stcok in {0} at yahoo finance".format(s))
    main(stock_list=s)

else:
    pass
