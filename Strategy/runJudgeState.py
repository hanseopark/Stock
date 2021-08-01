import datetime
import pandas as pd
import yahoo_fin.stock_info as yfs

from class_Strategy import ShortTermStrategy

def main (standard_symbol, index_list, index_name, start, end):

    strategy = ShortTermStrategy(standard_symbol, start, end)
    df_market = strategy.JudgeMarket()
    print(df_market)

    df_res = df_market.copy()
    df_res = df_res.reset_index()
    df_res = df_res.drop(['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Std', 'bol_upper', 'bol_down', 'MeanOfStd'], axis=1)
    df_res = df_res.loc[df_res.index[-1], :]

    print(df_res)

if __name__ == '__main__':
    td_1y = datetime.timedelta(weeks=52*2)
    today = datetime.datetime.now()
    start_day = today - td_1y

    dow_list = yfs.tickers_dow()
    filename = input("Choice of stock's list (dow, sp500, nasdaq, other, all, selected): ")
    if filename == 'dow':
        dow_list = yfs.tickers_dow()
        standard_index = 'DIA'
    elif filename == 'sp500':
        dow_list = yfs.tickers_sp500()
        standard_index = 'SPY'
    elif filename == 'nasdaq':
        dow_list = yfs.tickers_nasdaq()
        standard_index = 'QQQ'
    elif filename == 'other':
        dow_list = yfs.tickers_other()
        standard_index = '^DJI'
    elif filename == 'all':
        dow_list_1 = yfs.tickers_nasdaq()
        dow_list_2 = yfs.tickers_other()
        dow_list = dow_list_1 + dow_list_2
        standard_index = '^DJI'
    elif filename == 'selected':
        url = root_url+'/data_ForTrading/selected_ticker.json'
        temp_pd = pd.read_json(url)
        temp_pd = temp_pd['Ticker']
        dow_list = temp_pd.values.tolist()
        standard_index = '^DJI'

    main(standard_symbol = standard_index, index_list= dow_list, index_name = filename, start=start_day, end=today)
else:
    pass
