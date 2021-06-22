# I haven't yet understood thing.
# It is testing

#from Strategy.PlotStrategy import main as splt
#fig = splt('AAPL',False,'BB')
#fig.show()

#from Strategy.runStrategy import main as splt
from Strategy.runStrategy import main as srun
import yahoo_fin.stock_info as yfs
dow_list = yfs.tickers_dow()
#strategy = LongTermStrategy(symbol, start_day, now_day)
df_pred = srun(stock_list='dow', stats='ML')
print(df_pred)


