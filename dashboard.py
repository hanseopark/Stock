import streamlit as st
import yfinance as yf
import requests
import json
import numpy as np
import pandas_datareader as pdr
import pandas as pd
import matplotlib as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from iex import IEXStocks
from iex import YahooStocks
from PIL import Image

## Setting ##
st.set_option('deprecation.showPyplotGlobalUse', False)

symbol = st.sidebar.text_input("Symbol", value="AAPL")
day = st.sidebar.text_input('Day', value='2010-1-1')
symbol_list = ['^IXIC', symbol]
# symbol_list = ['AFL', 'BOP', 'GLD', 'SHY', 'IEF', 'AAPL']

#############################################################
# Time #
#############################################################
# start_day = datetime(2020,4,1)
start_day = day
end_day = datetime(2020,1,1)
now_day = datetime.today()

#############################################################
# For using API from IEX ,YahooFinance and mine
#############################################################
with open('config/stream.json', 'r') as f:
    config = json.load(f)

TOKEN_KEY = config['DEFAULT']['SECRET_KEY']
SANDBOX_KEY = config['TEST']['TEST_KEY']
#stock_IEX = IEXStocks(SANDBOX_KEY, symbol)
stock_IEX = IEXStocks(TOKEN_KEY, symbol)
# stock_Yahoo = YahooStocks(symbollist, start_day, now_day)
stock_Yahoo = YahooStocks(symbol_list, start_day, now_day)
#############################################################

screen = st.sidebar.selectbox("view", ('Overview', 'Fundamentals', 'News', 'Ownership', 'Technicals', 'Test'))

st.title(screen)

if screen == 'Overview':
    #logo = stock_IEX.get_logo()
    df = yf.download(symbol_list, start_day)['Adj Close']
    info = yf.Ticker(symbol).info
    df_quote = pdr.get_quote_yahoo(symbol)


    # For Beta using linear modeling
    price_change = df.pct_change() # Percentage Change Calculator
    df_ForBeta = price_change.drop(price_change.index[0])
    x = np.array(df_ForBeta['^IXIC']).reshape([-1,1])
    y = np.array(df_ForBeta[symbol])
    model = LinearRegression().fit(x, y)

    col1, col2 = st.beta_columns(2)
    with col1:
        #st.image(logo)
        st.subheader('Adj Close')
        st.line_chart(df)
        st.text_input('Beta:', model.coef_)
        st.text_input('Beta from quote: ', info['beta'])
        st.text_input('PER: ', df_quote['trailingPE'])
        st.text_input('PBR: ', df_quote['priceToBook'])

        st.line_chart(df_ForBeta)
        fig = sns.relplot(x=symbol, y='SPY', data=df_ForBeta)
        fig.ax.axline(xy1=(0.01,0.01), slope=1, color='b')
        st.pyplot()
        # st.write(df)
        # st.write(df['Adj Close'])
        # st.write(df_quote)
        # st.write(df_quote['priceToBook'])
        # st.write(info)
        # st.write(info['sector'])
        # st.write(df_quote)
        # st.write(df_ticker.astype('object'))
        # st.write(Ticker)
        # st.write(logo['url'])
        # st.write(info['logo_url'])
        # print(start_day)
        # print(r.info)
        # hist = r.history(period='5d')
        # st.image(logo['url'])

    with col2:
        st.subheader('Description')
        st.write(info['longBusinessSummary'])
        # print(end_day)
        # st.subheader(company_info['companyName'])
        # st.subheader('Description')
        # st.write(company_info['description'])
        # st.subheader('Industry')
        # st.write(company_info['industry'])
        # st.subheader('CEO')
        # st.write(company_info['CEO'])

if screen == 'Strategy':
    pass

if screen == 'Fundamentals':
    pass
    st.subheader('After corona')
    st.subheader('Beta')
# st.write(df_nasdaq_symbol.astype('object'))
# st.write(ticker_list[0])
# st.line_chart(df2['Adj Close'])
# st.write(df_quote['trailingPE']) # Price earing ratio (PER)
# df = pdr.DataReader(symbol,'yahoo',start_day,end_day)
# st.write(df)
# st.dataframe(df)
# stats = stock_IEX.get_statsj()
# chartj = stock_IEX.get_chart('1y')
# st.write(chart)
# for i in range
# st.write(chart[0]['close'])
# st.write(stats)

if screen == 'News':
    pass
    news = stock_IEX.get_news()
# for i in range (10):
# 	st.write('Headline')
# 	st.write(news[i]['headline'])
# 	st.write('Summary')
# 	st.write(news[i]['summary'])
# st.write(news[0])
# st.write(news)

if screen == 'Test':
    pass
#    # For NASDAQ ... about above 10000
#    # df_nasdaq_symbol = pdr.nasdaq_trader.get_nasdaq_symbols()
#    # ticker_list = df_nasdaq_symbol['NASDAQ Symbol'].values.tolist()
#    # stock_Yahoo_list = YahooStocks(ticker_list[200], start_day, now_day)
#    # df2 = stock_Yahoo_list.get_price_data()
#    # df_quote = pdr.get_quote_yahoo(symbol)
#
#
#    # For S&P500 ... about 500
#    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
#df_sp500 = pd.read_csv(url)
#    # pers_10 = pd.DataFrame({'PER':['']}, index=['Company'])
#    # pers_20 = pd.DataFrame({'PER':['']}, index=['Company'])
#    # error_symbols_per = []
#    # for c in df_sp500['Symbol']:
#    # 	try:
#    # 		per = pdr.get_quote_yahoo(c)['trailingPE']
#    # 		if per[c]<20:
#    # 			pers_20.loc[c] = per[c]
## 			if per[c]<10:
## 				pers_10.loc[c] = per[c]
##   	except:
#    # 		error_symbols_per.append(c)
#
#    # st.subheader('Low PER Strategy')
#    # st.text('PER < 10')
#    # st.write(pers_10)
#    # st.text('PER < 20')
#    # st.write(pers_20)
#
#    # For S%P5000 low PBR(price to book ratio)
#    df = pd.DataFrame({'PER':[], 'PBR':[], 'sector':[], 'Adj Close':[], 'DailyReturn':[]})
#    error_symbols_pbr =[]
#    for c in df_sp500['Symbol']:
#        try:
#            pass
#    # FOR REAL
#    # For pandas-datareader, the datatype is dataframe
#        df_quote = pdr.get_quote_yahoo(c)
#        per = df_quote['trailingPE']
#    # pbr = df_quote['priceToBookk']
#
#    # df_value = pdr.get_data_yahoo(c, start_day, nowday)
#    # Stock_value = df_value['Adj Close'] # index is times
#    # Stock_value_daily = Stock_value.pct_change()
#    # Stock_value_weekly = Stock.value.resample('7D').ffill().pct_channge
#    # Stock_value_weekly = Stock.value.resample('M').ffill().pct_channge
#
#    # # For yfinance, the datatype is dictionary
#    # dc_info = yf.Ticker(c).info
#    # GISD = dc_info['sector']
#
#    # # To make dataframe adding panadas-datareader+yfinance
#    # df.loc[c, 'PER'] = per[c]
#    # df.loc[c, 'PBR'] = pbr[c]
#    # df.loc[c, 'sector'] = GISD
#
#
#    # FOR TEST
##    if per[c] < 10:
##        df_value = pdr.get_data_yahoo(c, start_day, now_day)
##        Stock_value = df_value['Adj Close'] # index is times
##        Stock_value_daily = Stock_value.pct_change()
##        Stock_value_weekly = Stock.value.resample('7D').ffill().pct_channge
##        Stock_value_monthly = Stock.value.resample('M').ffill().pct_channge
##        daily_std = Stock_value_daily.std()* 252 ** 0.5
##        weekly_std = Stock_value_weekly.std() * 52 ** 0.5
##        monthly_std = Stock_value_monthly.std() * 12 ** 0.5
##
##        df.loc[c, 'PER'] = per[c]
##        df.loc[c, 'DailyReturn'] = daily_std
##        df.loc[c, 'WeeklyReturn'] = weekly_std
##        df.loc[c, 'MonthlyReturn'] = monthly_std
##
##        except:
##            error_symbols_pbr.append(c)
##
#
#    # df_value = pdr.get_data_yahoo(symbol, start_day, now_day)
#    # Stock_value = df_value['Adj Close'] # index is times
#    # Stock_value_daily = Stock_value.pct_change()
#    # daily_std = Stock_value_daily.std()* 252 ** 0.5
#    # df.loc[symbol, 'DailyReturn'] = daily_std
#
#    # st.subheader('Low PBR Strategy')
#    # pbrs = df['PER'].sort_values(by=['PBR'], axis=0)
#    # pbrs = pbrs.head(30)
#    # st.write(pbrs)
#
#    # list_GISD = []
#    # for c in pbrs.index:
#    # 	# df_GISD = yf.Ticker(c).info['sector']
#    # 	list_GISD.append(yf.Ticer(c).infor['sector'])
#    # 	# df.loc[c] =
#    # # df_GISD = yf.Ticker(pbrs).info('sector')
#    # st.write(df_GISD)
#    # st.write(df)
#    #st.write()
