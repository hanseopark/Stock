import pandas as pd
import pandas_datareader as pdr
import yahoo_fin.stock_info as yfs

import json

def main(url='', index_list = ['AAPL'], index_name = 'dow', EACH = True, ALL = True, SHOW = True, SAVE = True):

    ## Configuration directory url
    url_data = url+'data_origin/'
    url_pre  = url+'data_preprocessing/'

    strategy = LongTermStrategy(url, filename) # Select Long term strategy

    ###################
    ## Preprocessing ##
    ###################

    if EACH == True:
        print('Preprocessing each Financial Statements')
        # Basic stats
        dict_basic = {}
        basic_fac = ['PER', 'PSR', 'PBR', 'PEG', 'forPER', 'Cap']
        print('\nEach factor preprocessing in Basic stats ('+ ' '.join(s for s in basic_fac), end=')\n')
        for fac in basic_fac:
            if fac == 'PER':
                df = strategy.get_PER()
            elif fac == 'PSR':
                df = strategy.get_PSR()
            elif fac == 'PBR':
                df = strategy.get_PBR()
            elif fac == 'PEG':
                df = strategy.get_PEG()
            elif fac == 'forPER':
                df = strategy.get_FORPER()
            elif fac == 'Cap':
                df = strategy.get_CAP()

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(fac))
                df.to_json(url_pre+'/{0}_{1}.json'.format(index_name, fac))
                df.to_csv(url_pre+'/{0}_{1}.csv'.format(index_name, fac))

            if SHOW == True:
                print(df)
            dict_basic[fac] = df

        # Additional stats
        dict_add = {}
        basic_fac = ['Beta', 'DivRate', 'ROE', 'ROA', 'PM', 'Cash', 'Debt']
        print('\nEach factor preprocessing in Additional stats ('+ ' '.join(s for s in basic_fac), end=')\n')
        for fac in basic_fac:
            if fac == 'Beta':
                df = strategy.get_Beta()
            elif fac == 'DivRate':
                df = strategy.get_DivRate()
            elif fac == 'ROE':
                df = strategy.get_ROE()
            elif fac == 'ROA':
                df = strategy.get_ROA()
            elif fac == 'PM':
                df = strategy.get_PM()
            elif fac == 'Cash':
                df = strategy.get_Cash()
            elif fac == 'Debt':
                df = strategy.get_Debt()

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(fac))
                df.to_json(url_pre+'/{0}_{1}.json'.format(index_name, fac))
                df.to_csv(url_pre+'/{0}_{1}.csv'.format(index_name, fac))

            if SHOW == True:
                print(df)
            dict_add[fac] = df

        # Balance sheets
        dict_bal = {}
        basic_fac = ['TA']
        print('\nEach factor preprocessing in Balance sheets ('+ ' '.join(s for s in basic_fac), end=')\n')
        for fac in basic_fac:
            if fac == 'TA':
                df = strategy.get_TA()

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(fac))
                df.to_json(url_pre+'/{0}_{1}.json'.format(index_name, fac))
                df.to_csv(url_pre+'/{0}_{1}.csv'.format(index_name, fac))

            if SHOW == True:
                print(df)
            dict_bal[fac] = df

        # Income sheets
        dict_income = {}
        basic_fac = ['TR']
        print('\nEach factor preprocessing in Income sheets ('+ ' '.join(s for s in basic_fac), end=')\n')
        for fac in basic_fac:
            if fac == 'TR':
                df = strategy.get_TR()

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(fac))
                df.to_json(url_pre+'/{0}_{1}.json'.format(index_name, fac))
                df.to_csv(url_pre+'/{0}_{1}.csv'.format(index_name, fac))

            if SHOW == True:
                print(df)
            dict_income[fac] = df

        # Cash flow
        dict_flow = {}
        basic_fac = ['DIV', 'ISS']
        print('\nEach factor preprocessing in Cash flow ('+ ' '.join(s for s in basic_fac), end=')\n')
        for fac in basic_fac:
            if fac == 'DIV':
                df = strategy.get_DIV()
            elif fac == 'ISS':
                df = strategy.get_ISS()

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(fac))
                df.to_json(url_pre+'/{0}_{1}.json'.format(index_name, fac))
                df.to_csv(url_pre+'/{0}_{1}.csv'.format(index_name, fac))

            if SHOW == True:
                print(df)
            dict_flow[fac] = df

    if ALL == True:
        stats_name = ['stats', 'addstats', 'balsheets', 'income', 'flow']
        print('\nPreprocessing element in ('+ ' '.join(s for s in stats_name), end=')\n')
        for stat in stats_name:
            if stat == 'stats':
                df = strategy.get_stats(preprocessing = True)
            elif stat == 'addstats':
                df = strategy.get_addstats(preprocessing = True)
            elif stat == 'balsheets':
                df = strategy.get_balsheets_element(index_list)
            elif stat == 'income':
                df = strategy.get_income_element(index_list)
            elif stat == 'flow':
                df = strategy.get_flow_element(index_list)

            if SAVE == True:
                print('\n----------------------------- SAVE DATA  {} ---------------------------------\n'.format(stat))
                print('')
                df.to_json(url_pre+'/{0}_{1}_element.json'.format(index_name, stat))
                df.to_csv(url_pre+'/{0}_{1}_element.csv'.format(index_name, stat))

            if SHOW == True:
                print(df)

if __name__=='__main__':
    from class_Strategy import LongTermStrategy
    with open('config/config.json', 'r') as f:
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
        dow_list = temp_pd['Ticker'].values.tolist()

    main(url=root_url, index_list = dow_list, index_name = filename, EACH=True, ALL=True, SAVE=True, SHOW=False)

else:
    pass
