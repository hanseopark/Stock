import pandas as pd
import yahoo_fin.stock_info as yfs

import matplotlib.pyplot as plt

import datetime
import json
from tqdm import tqdm

from classModel import priceModel
from modelBB import ConditionBB

# Purpose: while running backtesting about backtest, how about earning and compare stadard index.

# 1. About every ticker in index Caclulating moving average.
# 1-1 save dictionary.
# 2. for date to slice
#       for ticker
# 3. it pass condition, selecting ticker.
# 4. Calculating earning to compare stndard index
# 5. Plot

def ConditionUp(ma5, ma20, ma60, ma120, upper, down, value, within, close):
    if upper < value: # Up to band
        return True

def daterange(start_date, end_date, step):
    end_date = end_date-5*datetime.timedelta(step)
    for n in range(0, int((end_date-start_date).days) +1, step):
        yield start_date+datetime.timedelta(n)

def main(url='', standard_symbol = '^IXIC',index_list=['aapl'], index_name='dow', start=datetime.datetime(2020,1,1), end=datetime.datetime.now()):
    url_data = url+'data_origin/'

    model = priceModel(url_data, index_name, start, end, Offline=False, run_yfs=True)

    # 1. About every ticker in index Caclulating moving average.
    # 1-1 save dictionary.

    df_date_ticker = {}
    error_symbols = []
    df_standard = model.with_moving_ave(standard_symbol)
    for ticker in tqdm(index_list):
        try:
            df_BB = model.with_moving_ave(ticker)
            df_date_ticker[ticker] = df_BB
        except:
            error_symbols.append(ticker)
    print(error_symbols)

    # 2. for date to slice
    #       for ticker
    df_ticker_cond = {}
    df_ticker_cal_1weak = {}
    df_ticker_cal_2weak = {}
    df_ticker_cal_3weak = {}
    earning_ave = [[],[],[]]
    earning_within2_ave = [[],[],[]]
    earning_within3_ave = [[],[],[]]
    earning_within4_ave = [[],[],[]]
    riseRate_within2 = []
    riseRate_within3 = []
    riseRate_within4 = []

    period=7

    for dt in tqdm(daterange(start, end, period)):
        earning_within2 = [[],[],[]]
        earning_within3 = [[],[],[]]
        earning_within4 = [[],[],[]]

        # 1 Weak
        df_standard_cal_1weak = df_standard.loc[dt+datetime.timedelta(period):dt+datetime.timedelta(2*period)]
        df_standard_cal_1weak_ago = df_standard_cal_1weak.iloc[0:1]
        df_standard_cal_1weak_recent = df_standard_cal_1weak.iloc[-1:]
        value_standard_cal_1weak_ago = float(df_standard_cal_1weak_ago['Open'].item())
        value_standard_cal_1weak_recent = float(df_standard_cal_1weak_recent['Adj Close'].item())

        # 2 Weak
        df_standard_cal_2weak = df_standard.loc[dt+datetime.timedelta(2*period):dt+datetime.timedelta(3*period)]
        df_standard_cal_2weak_ago = df_standard_cal_2weak.iloc[0:1]
        df_standard_cal_2weak_recent = df_standard_cal_2weak.iloc[-1:]
        value_standard_cal_2weak_ago = float(df_standard_cal_2weak_ago['Open'].item())
        value_standard_cal_2weak_recent = float(df_standard_cal_2weak_recent['Adj Close'].item())

        # 3 Weak
        df_standard_cal_3weak = df_standard.loc[dt+datetime.timedelta(3*period):dt+datetime.timedelta(4*period)]
        df_standard_cal_3weak_ago = df_standard_cal_3weak.iloc[0:1]
        df_standard_cal_3weak_recent = df_standard_cal_3weak.iloc[-1:]
        value_standard_cal_3weak_ago = float(df_standard_cal_3weak_ago['Open'].item())
        value_standard_cal_3weak_recent = float(df_standard_cal_3weak_recent['Adj Close'].item())

        for ticker in df_date_ticker.keys():
            df_ticker = df_date_ticker[ticker]
            df_ticker_cond[ticker] = df_ticker.loc[dt:dt+datetime.timedelta(period)]
            if df_ticker_cond[ticker].empty==False: # Checking datafrmae is not empty due to it is not exist at that time.
                # For condition
                df_ticker_cond_recent = df_ticker_cond[ticker].iloc[-1:]
                value_ticker_cond_recent = float(df_ticker_cond_recent['Adj Close'].item())
                upper_recent = float(df_ticker_cond_recent['bol_upper'].item())
                down_recent = float(df_ticker_cond_recent['bol_down'].item())
                ma5 = float(df_ticker_cond_recent['MA5'].item())
                ma20 = float(df_ticker_cond_recent['MA20'].item())
                ma60 = float(df_ticker_cond_recent['MA60'].item())
                ma120 = float(df_ticker_cond_recent['MA120'].item())

                # 1 Weak
                df_ticker_cal_1weak[ticker] = df_ticker.loc[dt+datetime.timedelta(period):dt+datetime.timedelta(2*period)]
                df_ticker_cal_1weak_ago = df_ticker_cal_1weak[ticker].iloc[0:1]
                df_ticker_cal_1weak_recent = df_ticker_cal_1weak[ticker].iloc[-1:]
                value_ticker_cal_1weak_ago = float(df_ticker_cal_1weak_ago['Adj Close'].item())
                value_ticker_cal_1weak_recent = float(df_ticker_cal_1weak_recent['Adj Close'].item())

                # 2 Weak
                df_ticker_cal_2weak[ticker] = df_ticker.loc[dt+datetime.timedelta(2*period):dt+datetime.timedelta(3*period)]
                df_ticker_cal_2weak_recent = df_ticker_cal_2weak[ticker].iloc[-1:]
                value_ticker_cal_2weak_recent = float(df_ticker_cal_2weak_recent['Adj Close'].item())

                # 3 Weak
                df_ticker_cal_3weak[ticker] = df_ticker.loc[dt+datetime.timedelta(3*period):dt+datetime.timedelta(4*period)]
                df_ticker_cal_3weak_recent = df_ticker_cal_3weak[ticker].iloc[-1:]
                value_ticker_cal_3weak_recent = float(df_ticker_cal_3weak_recent['Adj Close'].item())

                # 3. it pass condition, selecting ticker.
                # 4. Calculating earning to compare stndard index
                # 4-1 With average of earning,
                if ConditionBB(ma5, ma20, ma60, ma120, upper_recent, down_recent, value_ticker_cond_recent, 0.2, 0.015):
                    earning_1weak = (value_ticker_cal_1weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_2weak = (value_ticker_cal_2weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_3weak = (value_ticker_cal_3weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_within2[0].append(earning_1weak)
                    earning_within2[1].append(earning_2weak)
                    earning_within2[2].append(earning_3weak)

                if ConditionBB(ma5, ma20, ma60, ma120, upper_recent, down_recent, value_ticker_cond_recent, 0.3, 0.015):
                    earning_1weak = (value_ticker_cal_1weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_2weak = (value_ticker_cal_2weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_3weak = (value_ticker_cal_3weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_within3[0].append(earning_1weak)
                    earning_within3[1].append(earning_2weak)
                    earning_within3[2].append(earning_3weak)

                if ConditionBB(ma5, ma20, ma60, ma120, upper_recent, down_recent, value_ticker_cond_recent, 0.4, 0.015):
                    earning_1weak = (value_ticker_cal_1weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_2weak = (value_ticker_cal_2weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_3weak = (value_ticker_cal_3weak_recent-value_ticker_cal_1weak_ago)/value_ticker_cal_1weak_ago * 100
                    earning_within4[0].append(earning_1weak)
                    earning_within4[1].append(earning_2weak)
                    earning_within4[2].append(earning_3weak)

        if earning_within2[0]:
            for i in range(3):
                earning_within2_ave[i].append(sum(earning_within2[i])/len(earning_within2[i]))
        if earning_within3[0]:
            for i in range(3):
                earning_within3_ave[i].append(sum(earning_within3[i])/len(earning_within3[i]))
        if earning_within4[0]:
            for i in range(3):
                earning_within4_ave[i].append(sum(earning_within4[i])/len(earning_within4[i]))

        earning_1weak = (value_standard_cal_1weak_recent - value_standard_cal_1weak_ago)/value_standard_cal_1weak_ago * 100
        earning_2weak = (value_standard_cal_2weak_recent - value_standard_cal_1weak_ago)/value_standard_cal_1weak_ago * 100
        earning_3weak = (value_standard_cal_3weak_recent - value_standard_cal_1weak_ago)/value_standard_cal_1weak_ago * 100

        earning_ave[0].append(earning_1weak)
        earning_ave[1].append(earning_2weak)
        earning_ave[2].append(earning_3weak)

    if earning_within2_ave[0]:
        for i in range(3):
            riseRate_within2.append(sum(earning_within2_ave[i])/len(earning_within2_ave[i]))
    if earning_within3_ave[0]:
        for i in range(3):
            riseRate_within3.append(sum(earning_within3_ave[i])/len(earning_within3_ave[i]))
    if earning_within4_ave[0]:
        for i in range(3):
            riseRate_within4.append(sum(earning_within4_ave[i])/len(earning_within4_ave[i]))
    riseRate=[sum(earning_ave[0])/len(earning_ave[0]), sum(earning_ave[1])/len(earning_ave[1]), sum(earning_ave[2])/len(earning_ave[2])]

    print('Ascending of std    : ', riseRate)
    print('Ascending of spe 0.2: ', riseRate_within2)
    print('Ascending of spe 0.3: ', riseRate_within3)
    print('Ascending of spe 0.4: ', riseRate_within4)

    # 5. Plot
    fig, ax = plt.subplots()
    fig.suptitle('Close Band')
    idx = ['1Weak', '2Weak', '3Weak']
    ax.plot(idx, riseRate, label='index')
    ax.plot(idx, riseRate_within2, label='10%')
    ax.plot(idx, riseRate_within3, label='15%')
    ax.plot(idx, riseRate_within4, label='20%')

    plt.legend()
    plt.savefig(url+'Model/fig/TestingModelWithin.png')
    plt.show()

if __name__ == '__main__':
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']

    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all): \n")
    dow_list = yfs.tickers_dow()
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
        standard_index = '^DJI'
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
        standard_index = '^GSPC'
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
        standard_index = '^IXIC'
    elif filename == 'other':
        dow_list = yfs.tickers_other()
        standard_index = '^IXIC'
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
        standard_index = '^IXIC'
    print('--------------------------------------------------')
    print('-----------------', filename, '-------------------')
    print('--------------------------------------------------')

    start_day = datetime.datetime(2010,1,3)
    today = datetime.datetime.now()

    main(url=root_url, standard_symbol = standard_index, index_list=dow_list, index_name=filename, start = start_day, end = today)
else:
    pass
