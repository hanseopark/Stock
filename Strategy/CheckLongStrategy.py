import datetime
import os.path
import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import gridspec
import seaborn as sns

from tqdm import tqdm
import datetime
from class_Strategy import LongTermStrategy

print('It is true strategy of low PER is right?')

# Time range
#td_1y = datetime.timedelta(weeks=52/2)
td_1y = datetime.timedelta(weeks=52*2)
start_day = datetime.datetime(2010,1,1)
today = datetime.datetime.now()
#start_day = today - td_1y

# Get list of Dow tickers
dow_list = yfs.tickers_dow()
filename = ''
s= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
if s == 'dow':
    dow_list = yfs.tickers_dow()
    filename = 'dow'
    standard_index = '^DJI'
elif s == 'sp500':
    filename = 'sp500'
    dow_list = yfs.tickers_sp500()
    standard_index = '^GSPC'
elif s == 'nasdaq':
    filename = 'nasdaq'
    dow_list = yfs.tickers_nasdaq()
elif s == 'other':
    filename = 'other'
    dow_list = yfs.tickers_other()
elif s == 'selected':
    filename = 'selected'
    url = '/Users/hanseopark/Work/stock/data_ForTrading/selected_ticker.json'
    temp_pd = pd.read_json(url)
    temp_pd = temp_pd['Ticker']
    dow_list = temp_pd.values.tolist()

print('*'*100)
print(dow_list)
print('*'*100)

# Select strategy for situation
LimitValue = 0
url = '/Users/hanseopark/Work/stock/' # in data

stats = input('Choice statement (PER, PBR, Trend, ML, Pre): ')
if (stats == 'PER' or stats == "PBR"):
    strategy = LongTermStrategy(url, filename)
    s2 = input('Set {} point(10, 20, 30): '.format(stats))
    LimitValue = int(s2)
    inputname= 'origin'
elif (stats == 'ML' or 'Pre'):
    strategy = LongTermStrategy(url, filename)
    subname = 'preprocessing'

#elif (stats == 'Pre'):
#    strategy = LongTermStrategy(url, filename)

# Perform strategy and save
if (stats == 'PER' or stats == 'PBR'):
    url_threshold = url+'/data_origin/table{0}_{1}_{2}.json'.format(stats, filename,LimitValue)
    if (stats == 'PER'):
        df_per = strategy.LowPER(threshold = LimitValue)
    elif (stats == 'PBR'):
        df_per = strategy.LowPBR(threshold = LimitValue)
    df_per.to_json(url_threshold)
    list_per = df_per.index.to_list()

    df_st = pdr.DataReader(standard_index,'yahoo', start_day, today)
    init_st_price = df_st.loc[df_st.index[0], 'Adj Close']
    last_st_price = df_st.loc[df_st.index[-1], 'Adj Close']
    return_st_price = (last_st_price/init_st_price)*100
    list_return = []

    # Figure
    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(2,1,height_ratios=[1,1])
    ax_main = plt.subplot(gs[0])
    ax_1 = plt.subplot(gs[1])
    index = df_st.index.astype('str')
    def x_date(x,pos):
        try:
            return index[int(x-0.5)][:7]
        except IndexError:
            return ''
    ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

    #df_price = strategy.get_price_data(dow_list)
    df_price = strategy.get_price_data(list_per)
    print(df_price)

    for tic in tqdm(list_per):
        temp_df = df_price[df_price.Ticker == tic].copy()
        init_price = temp_df.loc[temp_df.index[0], 'Adj Close']
        last_price = temp_df.loc[temp_df.index[-1], 'Adj Close']
        return_price = (last_price/init_price)*100
        ax_main.plot(index, temp_df['Adj Close'], label=tic)
        # for ax_1
        list_return.append(return_price)

    # ax_main
    ax_main.plot(index, df_st['Adj Close'], label='Dow index (^DJI)')
    ax_main.legend(loc=2)
    ax_main.set_yscale('log')

    # ax_1
    ax_1.bar(list_per, list_return)
    ax_1.set_ylabel('Return (Last Price / Initial Price)')
    ax_1.axhline(y=return_st_price, color='r', label=standard_index)
    ax_1.axhline(y=sum(list_return)/len(list_return), color='g', label='Mean of tickers')
    ax_1.legend(loc=2)

    plt.show()

elif (stats == 'Pre' or 'ML'):
    dow_list = strategy.get_ticker_list()
    url_pre_price = url+'data_preprocessing/pre_{0}_Recent_price'.format(filename)
    url_pre_stats = url+'data_preprocessing/pre_{0}_stats'.format(filename)
    url_pre_addstats = url+'data_preprocessing/pre_{0}_addstats'.format(filename)
    url_pre_balsheets = url+'data_preprocessing/pre_{0}_balsheets'.format(filename)
    url_pre_income = url+'data_preprocessing/pre_{0}_income'.format(filename)
    url_pre_flow = url+'data_preprocessing/pre_{0}_flow'.format(filename)
    url_pre = url+'data_preprocessing/pre_{0}'.format(filename)

    if os.path.isfile(url_pre_price+'.csv'):
        s = input('The preprocessing data is already exist. If you want to analyze agian? (Y/N): ')
    else:
        s = 'Y'

    if s == 'yes' or s == 'Y' or s == 'Yes':
        # Price of stock
        #url_price = url+'FS_{0}_Value.json'.format(filename)
        df_price = strategy.get_price_data(etf_list=dow_list, OnlyRecent=True)
        df_price.to_json(url_pre_price+'.json')
        df_price.to_csv(url_pre_price+'.csv')

        # Rearange dataframe for preprocessing
        df_stats = strategy.get_stats_element(dow_list)
        df_stats.to_json(url_pre_stats+'.json')
        df_stats.to_csv(url_pre_stats+'.csv')

        df_addstats = strategy.get_addstats_element(dow_list)
        df_addstats.to_json(url_pre_addstats+'.json')
        df_addstats.to_csv(url_pre_addstats+'.csv')
        #print(df_addstats)

        df_balsheets = strategy.get_balsheets_element(dow_list)
        df_balsheets.to_json(url_pre_balsheets+'.json')
        df_balsheets.to_csv(url_pre_balsheets+'.csv')
        #print(df_balsheets)

        df_income = strategy.get_income_element(dow_list)
        df_income.to_json(url_pre_income+'.json')
        df_income.to_csv(url_pre_income+'.csv')
        #print(df_income)

        df_flow = strategy.get_flow_element(dow_list)
        df_flow.to_json(url_pre_flow+'.json')
        df_flow.to_csv(url_pre_flow+'.csv')
        #print(df_flow)

        df = pd.concat([df_price, df_stats, df_addstats, df_balsheets, df_income, df_flow], axis=1)
        df.dropna()
        #df.to_json(url_pre+'.json') # it has error
        df.to_csv(url_pre+'.csv')
        print(df)

    else:
        print('\n----------------------------- LOAD DATA ---------------------------------\n')
        df_price = pd.read_csv(url_pre_price+'.csv')
        df_stats = pd.read_csv(url_pre_stats+'.csv')
        df_addstats = pd.read_csv(url_pre_addstats+'.csv')
        df_balsheets = pd.read_csv(url_pre_balsheets+'.csv')
        df_income = pd.read_csv(url_pre_income+'.csv')
        df_flow = pd.read_csv(url_pre_flow+'.csv')
        df = pd.read_csv(url_pre+'.csv')

    if (stats == 'ML'):
        # Split data and test
        train_df, test_df = train_test_split(df, test_size=0.2)

        ## Correlation for features
        corrmat = train_df.corr()
        top_corr_features = corrmat.index[abs(corrmat['Recent_price'])>0.5]

        # Heatmap
        plt.figure(figsize=(12,8))
        plt_corr = sns.heatmap(train_df[top_corr_features].corr(), annot=True)
        plt.show()

