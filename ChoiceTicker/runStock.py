from StocksValue import main as stockvalue
from StocksInfo import main as stockinfo
import datetime

def main():
    ## Define time of start to end ##
    start_day = datetime.datetime(2010,1,1)
    today = datetime.datetime.now()

    ## running fucntion
    stats = ['dow', 'sp500', 'nasdaq']

    for s in stats:
        stockvalue(s, start_day, today)
        stockinfo(s)

if __name__ == '__main__':
    main()
else:
    pass
