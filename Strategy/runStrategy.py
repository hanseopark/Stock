import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import yahoo_fin.stock_info as yfs
import matplotlib.pyplot as plt
import seaborn as sns

import json
import datetime
from class_Strategy import LongTermStrategy, TrendStrategy

def main(stock_list=['dow'], stats = 'PER'):
    # Get datetime for price of stock
    td_1y = datetime.timedelta(weeks=52/2)
    #td_1y = datetime.timedelta(weeks=52*3)
    today = datetime.datetime.now()
    start_day = today - td_1y

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

    print('*'*100)
    print(dow_list)
    print('*'*100)

    url = '/Users/hanseopark/Work/stock/' # in data

    # Select strategy for situation
    LimitValue = 0
    if (stats == 'PER' or stats == "PBR"):
        strategy = LongTermStrategy(url, filename) # Select Long term strategy
        s2 = input('Set {} point(10, 20, 30): '.format(stats))
        LimitValue = int(s2)
    elif stats == 'Trend':
        #symbol = input('Write ticker name like aapl: ')
        #dow_list = [symbol]
        #strategy = TrendStrategy(symbol, start_day, today, keywords=dow_list)
        strategy = TrendStrategy(dow_list, start_day, today, keywords=dow_list)
    elif stats == 'ML':
        strategy = LongTermStrategy(url, filename) # Select Long term strategy

    # Perform strategy and save
    url_threshold = url+'/data_origin/table{0}_{1}_{2}'.format(stats, filename,LimitValue)
    if stats == 'PER':
        df_per = strategy.LowPER(threshold = LimitValue)
        #print(df_per)
        df_per.to_json(url_threshold+'.json')
        df_per.to_csv(url_threshold+'.csv')

    elif stats == 'PBR':
        df_pbr = strategy.LowPBR(threshold = LimitValue)
        #print(df_pbr)
        df_pbr.to_json(url_threshold+'.json')
        df_pbr.to_csv(url_threshold+'.csv')

    elif stats == 'Trend':
        # Getting price
        df_price = strategy.get_price_data(nomalization = True)
        #print(df_price)

        # Getting trend
        df_tr = strategy.get_trend_data()
        url_trend = url+'/data_origin/Trend_{0}'.format(filename)
        df_tr.to_json(url_trend+'.json')
        df_tr.to_csv(url_trend+'.csv')
        #print(df_tr)

        index = df_price.astype('str')
        fig = plt.figure(figsize=(10,10))
        ax_main = plt.subplot(1,1,1)

        def x_date(x,pos):
            try:
                return index[int(x-0.5)][:7]
            except indexerror:
                return ''

        # ax_main
        ax_main.xaxis.set_major_locator(ticker.maxnlocator(10))
        ax_main.xaxis.set_major_formatter(ticker.funcformatter(x_date))
        ax_main.set_title("Stock's value with google trend", fontsize=22 )
        #ax_main.plot(df_price['Adj Close'], label='ORLY')
        for tic in dow_list:
            ax_main.plot(df_tr[tic], label='Trend')
        ax_main.plot(df_price['Adj Close'], label="Stock's value")
        ax_main.legend(loc=2)

        plt.grid()
        plt.show()

    elif stats == 'ML':
        url = '/Users/hanseopark/Work/stock'
        df_price = strategy.get_price_data(etf_list = dow_list, OnlyRecent=True)
        SpecialStatements = True

        if SpecialStatements == True:
            ## Financial statement of stock
            df_stats = strategy.get_stats(preprocessing=True)
            df_addstats = strategy.get_addstats(True)
            df_balsheets = strategy.get_balsheets(True)
            df_income = strategy.get_income(True)
            df_flow = strategy.get_flow(True)

#            print(df_price)
#            print(df_stats)
#            print(df_addstats)
#            print(df_balsheets)
#            print(df_income)
#            print(df_flow)

            df = pd.concat([df_stats, df_addstats, df_balsheets, df_income, df_flow, df_price], axis=1)
            print(df)
            from pandas.api.types import is_numeric_dtype
            num_cols = [is_numeric_dtype(dtype) for dtype in df.dtypes]
            print(num_cols)

            # Split data and test For correlation
            from sklearn.model_selection import train_test_split
            train_df_corr, test_df_corr = train_test_split(df, test_size=0.2)

            # Correlation for features
            corrmat = train_df_corr.corr()
            top_corr_features = corrmat.index[abs(corrmat['Recent_price'])>0]
            print(top_corr_features)

            print(corrmat['Recent_price'].sort_values(ascending=False))

            # Heatmap
            plt.figure(figsize=(13,10))
            plt_corr = sns.heatmap(train_df_corr[top_corr_features].corr(), annot=True)

            plt.show()

            # Split target
#            train_y_label = train_df['Recent_price']
#            train_df = train_df.drop(['Recent_price'], axis=1, inplace=True)

            # How to considef NaN data
            # We need how to take the NaN data. First of all, we remove the NaN column over ratio of 0.5.
            nulltotal = df.isnull().sum().sort_values(ascending=False)
            nullpercent = ( df.isnull().sum() / len(df) ).sort_values(ascending=False)
            nullpoint = pd.concat([nulltotal, nullpercent], axis=1, keys=['Total number of null', 'Percent of null'])
            print(nullpoint)

            remove_cols = nullpercent[nullpercent >= 0.5].keys()
            df = df.drop(remove_cols, axis=1)
            print(df.isnull().sum().max())
            newtotal = df.isnull().sum().sort_values(ascending=False)
            print(newtotal)

            # filling the numeric data
            numeric_missed = ['Issuance', 'PER', 'ROE(%)', 'PBR', 'DividendsPaid']
            for feature in numeric_missed:
                df[feature] = df[feature].fillna(0)

            print('Re check')
            print(df.isnull().sum().max())


            ## Feature Engineering
            from scipy.stats import norm, skew
            numeric_feats = df.dtypes[df.dtypes != 'object'].index
            skewed_feats = df[numeric_feats].apply(lambda x: skew(x)).sort_values(ascending=False)
            high_skew = skewed_feats[abs(skewed_feats) > 0.5]
            print(high_skew)

            for feature in high_skew.index:
                df[feature] = np.log1p(df[feature]-df[feature].min()+1)

            # Split train and test for ML
#            y_df = df['Recent_price']
#            x_df = df.drop(['Recent_price'], axis=1 , inplace=True)
#            y_train, y_test, x_train, x_test = train_test_split(y_df, x_df, test_size=0.2)
#            print(y_train, y_test, x_train, x_test)

            train_df, test_df = train_test_split(df, test_size=0.2)
            y_train = train_df['Recent_price']
            x_train = train_df.iloc[:, :-1]
            y_test = test_df['Recent_price']
            x_test = test_df.iloc[:, :-1]
            test_index = x_test.index

            # Apply ML Model
#            from sklearn.metrics import make_scorer
#            from sklearn.model_selection import KFold, cross_val_score
#            from sklearn.metrics import mean_squared_error
#
#            scorer = make_scorer(mean_squared_error, greater_is_better = False)
#            def rmse_CV_train(model):
#                kf = KFold(5,shuffle=True,random_state=42).get_n_splits(x_train.values)
#                rmse = np.sqrt(-cross_val_score(model, x_train, y_train,scoring ="neg_mean_squared_error",cv=kf))
#                return (rmse)
#
#            def rmse_CV_test(model):
#                kf = KFold(5,shuffle=True,random_state=42).get_n_splits(train.values)
#                rmse = np.sqrt(-cross_val_score(model, x_test, y_test,scoring ="neg_mean_squared_error",cv=kf))
#                return (rmse)

            import xgboost as XGB

            the_model = XGB.XGBRegressor(colsample_bytree=0.4603, gamma=0.0468,
                                        learning_rate=0.05, max_depth=3,
                                        min_child_weight=1.7817, n_estimators=2200,
                                        reg_alpha=0.4640, reg_lambda=0.8571,
                                        subsample=0.5213, random_state =7, nthread = -1)
            the_model.fit(x_train, y_train)
            y_pred = the_model.predict(x_test)
            print('Predction: ', y_pred)
            y_predict = np.floor(np.expm1(the_model.predict(x_test)))
            print('Prediction: ', y_predict)

            print(y_test)
            sub = pd.DataFrame()
            sub['Ticker'] = test_index
            sub['Price of Prediction'] = y_predict
            sub = sub.set_index('Ticker')
            sub_new = pd.concat([sub, y_test], axis=1)
            print(sub)

        else:
            df_stats = strategy.get_stats_element(dow_list)
            df_addstats = strategy.get_addstats_element(dow_list)
            df_balsheets = strategy.get_balsheets_element(dow_list)
            df_income = strategy.get_income_element(dow_list)
            df_flow = strategy.get_flow_element(dow_list)
            df = pd.concat([df_stats, df_addstats, df_balsheets, df_income, df_flow, df_price], axis=1)
            print(df)

            print(df.dtypes)
            from pandas.api.types import is_numeric_dtype
            num_cols = [is_numeric_dtype(dtype) for dtype in df.dtypes]
            print(num_cols)

#            for _ in df.columns:
#                print(df[_].type)

#            # Split
#            from sklearn.model_selection import train_test_split
#            train_x, val_x, train_y, val_y = train_test_split(df, df_price, test_size=0.2)
#            #train_df.head(5), test_df.head(5)
#
#            # Scaling
#            from mlxtend.preprocessing import minmax_scaling
#            x_scaled =minmax_scaling(df, columns=df.columns)
#
#            train_xs, val_xs, trains_ys, val_ys = train_test_split(x_scaled, df_prcie, test_size=0.2)
#
#            # Features
#            yf = df_price.Recent_price
#            xf = df
#
#            # Label encoding for categoricals
#            for colname in xf.select_dtype("object"):
#                xf[colname], _ = xf[colname].factorize()
#
#            # All discrete features should now have integer dtypes (double-check this before using MI!)
#            discrete_features = xf.dtypes == int




if __name__ == '__main__':
    s_list= input("Choice of stock's list (dow, sp500, nasdaq, other, selected): ")
    statements = input('Choice statement (PER, PBR, Trend, ML): ')
    main(stock_list=s_list, stats=statements)

else:
    pass









