import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs

from tqdm import tqdm
import datetime
import json

def main(url, index_list, index_name, start, end, run_yfs=False, run_pdr=True):

    ## Configuration directory url
    url_data = url+'data_origin/'

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
            df_recent.loc[ticker, 'Recent_price'] = yfs.get_live_price(ticker)

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

    url_value_data = url_data+'FS_{0}_Value'.format(index_name)
    combined_value.to_json(url_value_data+'.json')
    combined_value.to_csv(url_value_data+'.csv')

    url_recent_value_data = url_data+'FS_{0}_Recent_Value'.format(index_name)
    df_recent.to_json(url_recent_value_data+'.json')
    df_recent.to_csv(url_recent_value_data+'.csv')

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
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

    ## Define time of start to end ##
    #td_1y = datetime.timedelta(weeks=52/2)
    start_day = datetime.datetime(2010,1,1)
    today = datetime.datetime.now()
    #start_day = today-td_1y

    print('Price of stcok in {0} for date series and recent price'.format(filename))
    main(url=root_url, index_list = dow_list, index_name=filename, start= start_day, end = today, run_yfs = True, run_pdr=False)

else:
    pass
