import yahoo_fin.stock_info as yfs
import pandas as pd

from tqdm import tqdm
import json

def main(url, standard_symbol, index_list, index_name):

    ## Configuration directory url
    url_data = url+'data_origin/'

    # For check the table of one ticker like aapl
    #aapl_quote = yfs.get_quote_table(standard_symbol)
    aapl_quote = yfs.get_financials(standard_symbol, yearly = False, quarterly = True)
    #aapl_val = yfs.get_stats_valuation(standard_symbol)
#    aapl_ext = yfs.get_stats(standard_symbol)
#    aapl_sheet = yfs.get_balance_sheet(standard_symbol)
#    aapl_income = yfs.get_income_statement(standard_symbol)
#    aapl_flow = yfs.get_cash_flow(standard_symbol)

    print('*'*100)
    print('quote')
    print(aapl_quote['quarterly_cash_flow'])
    print('*'*100)
#    print('basic')
#    print(aapl_val)
#    print('*'*100)
#    print('additional')
#    print(aapl_ext)
#    print('*'*100)
#    print('balance sheets')
#    print(aapl_sheet)
#    print(len(aapl_sheet.columns))
#    print('*'*100)
#    print('income statements')
#    print(aapl_income)
#    print('*'*100)
#    print('cash flow')
#    print(aapl_flow)
#    print('*'*100)

    # Get data in the current  olumn for each stock's valuation table
    dow_stats = {}
    dow_addstats = {}
    dow_balsheets = {}
    dow_income = {}
    dow_flow = {}

    error_symbols = []
    for ticker in tqdm(index_list):
        try:
            # Getteing Summary
            basic = yfs.get_stats_valuation(ticker)
            basic =basic.iloc[:,:2]
            basic.columns = ['Attribute', 'Recent']
            dow_stats[ticker] = basic

            # Getting additioanl stats
            add = yfs.get_stats(ticker)
            add.columns = ['Attribute', 'Value']
            dow_addstats[ticker] = add

            financial_stats = yfs.get_financials(ticker, yearly = False, quarterly=True)
            # Getting balance sheets
            sheets = financial_stats['quarterly_balance_sheet']
            dow_balsheets[ticker] = sheets

            # Getting income statements
            income = financial_stats['quarterly_income_statement']
            dow_income[ticker] = income

            # Getting cash flow statements
            flow = financial_stats['quarterly_cash_flow']
            dow_flow[ticker] = flow

        except:
            error_symbols.append(ticker)
            print('Error ticker: ', ticker)

    print('error symol: ', error_symbols)

    for ticker in dow_balsheets.keys():
        leng = len(dow_balsheets[ticker].columns)
        dow_balsheets[ticker].columns = ['Before_'+str(i) for i in range(0,leng)]
        dow_balsheets[ticker] = dow_balsheets[ticker].rename(columns={'Before_0': 'Recent'})

    for ticker in dow_income.keys():
        leng = len(dow_income[ticker].columns)
        dow_income[ticker].columns = ['Before_'+str(i) for i in range(0,leng)]
        dow_income[ticker] = dow_income[ticker].rename(columns={'Before_0': 'Recent'})

    for ticker in dow_flow.keys():
        leng = len(dow_flow[ticker].columns)
        dow_flow[ticker].columns = ['Before_'+str(i) for i in range(0,leng)]
        dow_flow[ticker] = dow_flow[ticker].rename(columns={'Before_0': 'Recent'})


    combined_stats = pd.concat(dow_stats)
    combined_stats = combined_stats.reset_index()
    combined_stats = combined_stats.rename(columns={'level_0': 'Ticker'})

    combined_addstats = pd.concat(dow_addstats)
    combined_addstats = combined_addstats.reset_index()
    combined_addstats = combined_addstats.rename(columns={'level_0': 'Ticker'})

    combined_balsheets = pd.concat(dow_balsheets)
    combined_balsheets = combined_balsheets.reset_index()
    combined_balsheets = combined_balsheets.rename(columns={'level_0': 'Ticker'})

    combined_income = pd.concat(dow_income)
    combined_income = combined_income.reset_index()
    combined_income = combined_income.rename(columns={'level_0': 'Ticker'})

    combined_flow = pd.concat(dow_flow)
    combined_flow = combined_flow.reset_index()
    combined_flow = combined_flow.rename(columns={'level_0': 'Ticker'})

    del combined_stats['level_1']
    del combined_addstats['level_1']

    print(combined_stats)
    print(combined_addstats)
    print(combined_balsheets)
    print(combined_income)
    print(combined_flow)

    list_stats = ['stats', 'addstats', 'balsheets', 'income', 'flow']
    for s in list_stats:
        url_FS = url_data+'FS_{0}_{1}'.format(index_name, s)
        if s == 'stats':
            df = combined_stats
        elif s == 'addstats':
            df = combined_addstats
        elif s == 'balsheets':
            df = combined_balsheets
        elif s == 'income':
            df = combined_income
        elif s == 'flow':
            df = combined_flow
        df.to_json(url_FS+'.json')
        df.to_csv(url_FS+'.csv')

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")

    # Get list of Dow tickers
    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
        standard_index = '^DJI'
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
        standard_index = 'aapl'
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
        standard_index = '^IXIC'
    elif filename == 'other':
        dow_list = yfs.tickers_other()
        standard_index = '^IXIC'
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()
        standard_index = '^IXIC'

    print('--------------------------------------------------')
    print('-----------------', filename, '-------------------')
    print('--------------------------------------------------')

    main(url=root_url, standard_symbol = standard_index, index_list = dow_list, index_name = filename)

else:
    pass
