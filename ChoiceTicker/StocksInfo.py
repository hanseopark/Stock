import yahoo_fin.stock_info as yfs
import pandas as pd
from tqdm import tqdm

def main(stock_list):
    # For check the table of one ticker like aapl
    aapl_quote = yfs.get_quote_table('aapl')
    aapl_val = yfs.get_stats_valuation('aapl')
    aapl_ext = yfs.get_stats('aapl')
    aapl_sheet = yfs.get_balance_sheet('aapl')
    aapl_income = yfs.get_income_statement('aapl')
    aapl_flow = yfs.get_cash_flow('aapl')

    print('*'*100)
    print('quote')
    print(aapl_quote)
    print('*'*100)
    print('basic')
    print(aapl_val)
    print('*'*100)
    print('additional')
    print(aapl_ext)
    print('*'*100)
    print('balance sheets')
    print(aapl_sheet)
    print(len(aapl_sheet.columns))
    print('*'*100)
    print('income statements')
    print(aapl_income)
    print('*'*100)
    print('cash flow')
    print(aapl_flow)
    print('*'*100)

    # Get list of Dow tickers
    dow_list = yfs.tickers_dow()
    filename = ''
    if stock_list == 'dow':
        dow_list = yfs.tickers_dow()
        filename = 'dow'
    elif stock_list == 'sp500':
        filename = 'sp500'
        dow_list = yfs.tickers_sp500()
    elif stock_list == 'nasdaq':
        filename = 'nasdaq'
        dow_list = yfs.tickers_nasdaq()
    elif stock_list == 'other':
        filename = 'other'
        dow_list = yfs.tickers_other()
    elif stock_list == 'selected':
        filename = 'selected'
        url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()

    print(dow_list)

    # Get data in the current  olumn for each stock's valuation table
    dow_stats = {}
    dow_addstats = {}
    dow_balsheets = {}
    dow_income = {}
    dow_flow = {}

    error_symbols = []
    for ticker in tqdm(dow_list):
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

            # Getting balance sheets
            sheets = yfs.get_balance_sheet(ticker)
            dow_balsheets[ticker] = sheets

            # Getting income statements
            income = yfs.get_income_statement(ticker)
            dow_income[ticker] = income

            # Getting cash flow statements
            flow = yfs.get_cash_flow(ticker)
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
        url = '/Users/hanseopark/Work/stock/data_origin/FS_{0}_{1}'.format(filename, s)
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
        df.to_json(url+'.json')
        df.to_csv(url+'.csv')

if __name__ == '__main__':
    s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
    main(stock_list=s)

else:
    pass
