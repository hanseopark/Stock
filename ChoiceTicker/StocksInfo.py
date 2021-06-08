import yahoo_fin.stock_info as yfs
import pandas as pd
from tqdm import tqdm

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
s= input("Choice of stock's list (dow, sp500, nasdaq, other): ")
if s == 'dow':
    dow_list = yfs.tickers_dow()
    filename = 'dow'
elif s == 'sp500':
    filename = 'sp500'
    dow_list = yfs.tickers_sp500()
elif s == 'nasdaq':
    filename = 'nasdaq'
    dow_list = yfs.tickers_nasdaq()
elif s == 'other':
    filename = 'other'
    dow_list = yfs.tickers_other()
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
        #basic = FinancialStatements(ticker).get_Basic()
        basic = yfs.get_stats_valuation(ticker)
        basic =basic.iloc[:,:2]
        basic.columns = ['Attribute', 'Recent']
        dow_stats[ticker] = basic

        # Getting additioanl stats
        #add = FinancialStatements(ticker).get_Add()
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

recent_sheets = {ticker : sheet.iloc[:,:1] for ticker, sheet in dow_balsheets.items()}
for ticker in recent_sheets.keys():
    recent_sheets[ticker].columns = ["Recent"]

recent_income_statements = {ticker : sheet.iloc[:,:1] for ticker,sheet in dow_income.items()}
for ticker in recent_income_statements.keys():
    recent_income_statements[ticker].columns = ["Recent"]

recent_cash_flows = {ticker : flow.iloc[:,:1] for ticker,flow in dow_flow.items()}
for ticker in recent_cash_flows.keys():
    recent_cash_flows[ticker].columns = ["Recent"]


combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()

combined_addstats = pd.concat(dow_addstats)
combined_addstats = combined_addstats.reset_index()

combined_balsheets = pd.concat(recent_sheets)
combined_balsheets = combined_balsheets.reset_index()

combined_income = pd.concat(recent_income_statements)
combined_income = combined_income.reset_index()

combined_flow = pd.concat(recent_cash_flows)
combined_flow = combined_flow.reset_index()

del combined_stats['level_1']
del combined_addstats['level_1']

combined_stats.columns = ['Ticker', 'Attribute', 'Recent']
combined_addstats.columns = ['Ticker', 'Attribute', 'Value']
combined_balsheets.columns = ['Ticker', 'Breakdown', 'Recent']
combined_income.columns = ["Ticker", "Breakdown", "Recent"]
combined_flow.columns = ["Ticker", "Breakdown", "Recent"]

print(combined_stats)
print(combined_addstats)
print(combined_balsheets)
print(combined_income)
print(combined_flow)

list_stats = ['stats', 'addstats', 'balsheets', 'income', 'flow']
#url = '../data/FS_{0}_{1}'.format(filename,stats)
for s in list_stats:
    url = '../data/FS_{0}_{1}.json'.format(filename, s)
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
    df.to_json(url)






