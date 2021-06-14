import datetime
import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import gridspec

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
url = '/Users/hanseopark/Work/stock/data_origin/' # in data

stats = input('Choice statement (PER, PBR, Trend, ML): ')
if (stats == 'PER' or stats == "PBR"):
    strategy = LongTermStrategy(url, filename)
    s2 = input('Set {} point(10, 20, 30): '.format(stats))
    LimitValue = int(s2)

# Perform strategy and save
url_threshold = '/Users/hanseopark/Work/stock/data_origin/table{0}_{1}_{2}.json'.format(stats, filename,LimitValue)
df_per = strategy.LowPER(threshold = LimitValue)
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

