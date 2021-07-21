import numpy as np
import pandas as pd
import yahoo_fin.stock_info as yfs

import matplotlib.pyplot as plt
import seaborn as sns
import json

def main(url = '', index_list = ['AAPL'], index_name = 'dow', portfolio=['AAPL']):

    ## Load Financial statement of stock preprocessed
    df_stats = pd.read_json(url+'/data_preprocessing/{0}_stats_element.json'.format(index_name))
    df_addstats = pd.read_json(url+'/data_preprocessing/{0}_addstats_element.json'.format(index_name))
    df_balsheets = pd.read_json(url+'/data_preprocessing/{0}_balsheets_element.json'.format(index_name))
    df_income = pd.read_json(url+'/data_preprocessing/{0}_income_element.json'.format(index_name))
    df_flow = pd.read_json(url+'/data_preprocessing/{0}_flow_element.json'.format(index_name))

    ## Merge dataframe
    df = pd.concat([df_stats, df_addstats, df_balsheets, df_income, df_flow], axis=1)

    ## Chech numerice datasets
    from pandas.api.types import is_numeric_dtype
    num_cols = [is_numeric_dtype(dtype) for dtype in df.dtypes]

    # Split data and test For correlation
    from sklearn.model_selection import train_test_split
    train_df_corr, test_df_corr = train_test_split(df, test_size=0.2)

    # Correlation for features
    corrmat = train_df_corr.corr()
    top_corr_features = corrmat.index[abs(corrmat['marketCap'])>0]
    #print(top_corr_features)

    # Heatmap
    plt.figure(figsize=(13,10))
    plt_corr = sns.heatmap(train_df_corr[top_corr_features].corr(), annot=True)

    plt.savefig(url+'/Model/ML/corrHeatmap_{0}.eps'.format(index_name))
    #plt.show()

    #########################################################################
    # How to considef NaN data
    # We need how to take the NaN data. First of all, we remove the NaN column over ratio of 0.5.

    ####################
    ### Remove index ###
    ####################
    print("###### NAN #######")
    print('Before removing index: ', len(df))
    df = df[df['marketCap'].notna()]
    df_index_null = pd.DataFrame(columns=['TotalNull', 'PercentOfNull'])
    for ticker in df.index:
        temp_df = df.loc[ticker,:]
        count_null = temp_df.isnull().sum()
        percent_count_null = count_null/len(temp_df)
        df_index_null.loc[ticker, 'TotalNull'] = count_null
        df_index_null.loc[ticker, 'PercentOfNull'] = percent_count_null

    remove_index = df_index_null[df_index_null['PercentOfNull']>0.5].index.tolist()
    #print(len(remove_index))

    ## For portlist
    unequal_in_index = [x for x in portfolio if x not in df.index.values.tolist()]
    for l in unequal_in_index:
        portfolio.remove(l)
    for tic in portfolio:
        if tic in remove_index:
            remove_index.remove(tic)
    df = df.drop(remove_index, axis=0)
    print('After removing index: ', len(df))

    ######################
    ### Remove columns ###
    ######################
    print('Before removing columns: ', len(df.columns))

    nulltotal = df.isnull().sum().sort_values(ascending=False)
    nullpercent = ( df.isnull().sum() / len(df) ).sort_values(ascending=False)
    nullpoint = pd.concat([nulltotal, nullpercent], axis=1, keys=['Total number of null', 'Percent of null'])
    remove_cols = nullpercent[nullpercent >= 0.5].keys()
    df = df.drop(remove_cols, axis=1)
    newtotal = df.isnull().sum().sort_values(ascending=False)

    print('After removing columns: ', len(df.columns))

    # Filling the numeric data
    numeric_missed = newtotal.index
    #numeric_missed = ['minorityInterest', 'PER', 'ROE(%)', 'PBR', 'DividendsPaid']
    for feature in numeric_missed:
        df[feature] = df[feature].fillna(0)

    ## Feature Engineering
    from scipy.stats import norm, skew
    numeric_feats = df.dtypes[df.dtypes != 'object'].index
    skewed_feats = df[numeric_feats].apply(lambda x: skew(x)).sort_values(ascending=False)
    high_skew = skewed_feats[abs(skewed_feats) > 0.5]
    #print('High feature')
    #print(high_skew)

#   print("********"*10)
#   print(df)
#   for feature in high_skew.index:
#       df[feature] = np.log1p(df[feature]-df[feature].min()+1)

    print("********"*10)
    print(df)
    print("********"*10)
    print(df['marketCap'].copy())

    # Split train and test for ML

    # Taget setting
    y_df = df['marketCap']
    df = df.drop(['marketCap'], axis=1)

    y_df = y_df.to_frame()
    #y_train, y_test, x_train, x_test = train_test_split(y_df, df, test_size=0.2)
#print(y_train, y_test, x_train, x_test)

    y_test = y_df.loc[y_df.index.intersection(portfolio), :]
    x_test = df.loc[df.index.intersection(portfolio), :]
    y_train = y_df.drop(portfolio, axis=0)
    x_train = df.drop(portfolio, axis=0)

    test_index = x_test.index
    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.metrics import mean_squared_error

#   scorer = make_scorer(mean_squared_error, greater_is_better = False)
#   def rmse_CV_train(model):
#       kf = KFold(5,shuffle=True,random_state=42).get_n_splits(x_train.values)
#       rmse = np.sqrt(-cross_val_score(model, x_train, y_train,scoring ="neg_mean_squared_error",cv=kf))
#       return (rmse)
#
#   def rmse_CV_test(model):
#       kf = KFold(5,shuffle=True,random_state=42).get_n_splits(train.values)
#       rmse = np.sqrt(-cross_val_score(model, x_test, y_test,scoring ="neg_mean_squared_error",cv=kf))
#       return (rmse)

    import xgboost as XGB

    model = XGB.XGBRegressor(colsample_bytree=0.4603, gamma=0.0468,
                         learning_rate=0.05, max_depth=3,
                         min_child_weight=1.7817, n_estimators=2200,
                         reg_alpha=0.4640, reg_lambda=0.8571,
                         subsample=0.5213, random_state =7, nthread = -1)
    # To solve error
    x_train = x_train.loc[:,~x_train.columns.duplicated()]
    duplicate_columns = x_train.columns[x_train.columns.duplicated()]
    x_test = x_test.loc[:,~x_test.columns.duplicated()]
    duplicate_columns_t = x_test.columns[x_test.columns.duplicated()]
    model.fit(x_train, y_train)

    #y_predict = np.floor(np.expm1(model.predict(x_test)))
    y_predict = np.floor(model.predict(x_test))

    predictions = [round(value) for value in model.predict(x_test)]

    print('Prediction')
    print(y_predict)
    print('y value of test')
    print(y_test)

    sub = pd.DataFrame()
    sub['Ticker'] = test_index
    sub['PredictionOfMarket'] = y_predict
    sub = sub.set_index('Ticker')
    sub = pd.concat([sub, y_test], axis=1)
    sub['ratio'] = sub.PredictionOfMarket / sub.marketCap
    sub = sub.sort_values(by= 'ratio', ascending=False)
    #print(corrmat['Recent_price'].sort_values(ascending=False))
    print(sub)
#   kfold = KFold(n_splits=10, random_state=7)
#   results = cross_val_score(model, x_test, y_test, cv=kfold)
#   print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

    acc = mean_squared_error(y_test, predictions)
    print('mse: ', acc)
    model.save_model(url+'/Model/ML/model_{0}.json'.format(index_name))

    ## Test Load model ##
#   test_model = XGB.XGBRegressor()
#   test_model.load_model(url+'/Model/ML/model_{0}.json'.format(index_name))
#   print(test_model.predict(x_test))

    print('The ratio over 10: ')
    print(sub[sub['ratio']>10])

    return sub

if __name__=='__main__':
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
    root_url = config['root_dir']
    dow_list = yfs.tickers_dow()
    filename= input("Choice of stock's list (dow, sp500, nasdaq, other, all, selected): ")
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
    elif filename == 'other':
        dow_list = yfs.tickers_other()
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()

    port_input = input('set portpolio: (lowper, energy, dow, sp500, mine) ')
    if port_input == 'energy':
        energy_list = ['APA', 'COG', 'COP', 'CVX', 'DVN', 'EOG', 'FANG', 'HAL', 'HES', 'KMI', 'MPC', 'MRO', 'NOV', 'OKE', 'OXY', 'PSX', 'PXD', 'SLB', 'VLO', 'WMB', 'XOM']
        port_list = energy_list
    elif port_input == 'lowper':
        df_low_per = main(stock_list=filename, stats = 'PER', Limit = 5)
        lowper_list = df_low_per.index.values.tolist()
        port_list = lowper_list
    elif port_input == 'mine':
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list
    elif port_input == 'dow':
        my_list = yfs.tickers_dow()
        port_list = my_list
    elif port_input == 'sp500':
        my_list = yfs.tickers_sp500()
        port_list = my_list
    else:
        my_list = ['AAPL', 'NFLX', 'TSM', 'ZIM', 'BP', 'MRO']
        port_list = my_list

    print('In my portfolio: ', port_list)

    main(url=root_url, index_list=dow_list, index_name = filename, portfolio = port_list)

else:
    pass

