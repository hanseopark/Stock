import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs

from tqdm import tqdm
import datetime

def main(index_name, start, end, run_yfs=False, run_pdr=True):

    index_list = yfs.tickers_dow()
    if index_name == 'dow':
        index_list = yfs.tickers_dow()
    elif index_name == 'sp500':
        index_list = yfs.tickers_sp500()
    elif index_name == 'nasdaq':
        index_list = yfs.tickers_nasdaq()
    elif index_name == 'other':
        index_list = yfs.tickers_other()
    elif index_name == 'selected':
        url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        index_list = temp_pd.values.tolist()

    print(index_list)

    print('Example Apple inc')
    if run_pdr:
        df_aapl = pdr.DataReader('AAPL', 'yahoo', start_day, today)

    if run_yfs:
        start_day.strftime('%m/%d/%y')
        today.strftime('%m/%d/%y')
        df_aapl = yfs.get_data('AAPL',start_date=start_day, end_date = today)
        df_aapl = df_aapl.reset_index()
        df_aapl = df_aapl.rename(columns={'open':'Open', 'index':'Date', 'high':'High','low':'Low','close':'Close','adjclose':'Adj Close','volume':'Volume','ticker':'Ticker'})
        df_aapl = df_aapl[['Ticker','Date','High','Low','Open','Close','Volume','Adj Close']]
    print(df_aapl)

    df_recent = pd.DataFrame({'Recent_price': []})
    etf_values = {}
    error_symbols = []
    for ticker in tqdm(index_list):
        try:
            if run_pdr:
                df = pdr.DataReader(ticker,'yahoo', start_day, today)
            if run_yfs:
                df = yfs.get_data(ticker,start_date=start_day, end_date = today)
                df = df.reset_index()
                df = df.rename(columns={'open':'Open', 'index':'Date', 'high':'High','low':'Low','close':'Close','adjclose':'Adj Close','volume':'Volume','ticker':'Ticker'})
                df = df[['Ticker','Date','High','Low','Open','Close','Volume','Adj Close']]
            df_recent.loc[ticker, 'Recent_price'] = yfs.get_live_price(ticker)
            etf_values[ticker] = df
        except:
            error_symbols.append(ticker)
    print('Error: ', error_symbols)

    if run_pdr:
        combined_value = pd.concat(etf_values)
        combined_value = combined_value.reset_index()
        combined_value= combined_value.rename(columns={'level_0': 'Ticker'})
    if run_yfs:
        combined_value = pd.concat(etf_values)
        combined_value = combined_value.reset_index()
        combined_value = combined_value.drop(['level_0','level_1'], axis=1)

    print(combined_value)
    print(df_recent)

    url = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_Value'.format(index_name)
    combined_value.to_json(url+'.json')
    combined_value.to_csv(url+'.csv')

    url_recent = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_Recent_Value'.format(index_name)
    df_recent.to_json(url_recent+'.json')
    df_recent.to_csv(url_recent+'.csv')

if __name__ == '__main__':
    s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")

    ## Define time of start to end ##
    #td_1y = datetime.timedelta(weeks=52/2)
    start_day = datetime.datetime(2010,1,1)
    today = datetime.datetime.now()
    #start_day = today-td_1y

    print('Price of stcok in {0} for date series and recent price'.format(s))
    main(index_name=s, start= start_day, end = today, run_yfs = True, run_pdr=False)

else:
    pass
