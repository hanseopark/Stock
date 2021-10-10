# Stock
It is my toy model for applying calculation of stock.

### Bolinger Bands
The bolinger band is used by std of each ticker in BolingerBands directory.

### RelativeStrengthIndex
This model is made by RSI point

### ChoiceTicker
It is explained to daownload s&p500 and nasdaq tickers from package of both yfinnace and yahoo_fin.stock_info.

### CombineDataFrame
It is combined from dataframe calculated by strategy

### Strategy
It is explained how to choose ticker in condition like PER and PBR

### Model
There are modeling idea to get strategy. The examples are BB, RSI and High value etc...
The idea will be updated more.

### Dashboard
If you want to see the visulizaion of data using streamlit, you have to get the token key of API.

$ streamlit run dashbord.py

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fhanseopark%2FStock&count_bg=%2379C83D&title_bg=%23555555&icon=xampp.svg&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## Script
### Modeling and Downloading
$ bash runAnalysis.sh y y 
{1} is meaning to do runGET.sh and {2} is meaning to do runModel.

### Get stock's value, information with financial statements
$ bash runGET.sh dow
we can change the index from dow to **sp500, nasdaq and other** which are included NYSE and others

### Get ticker using Model that is applied BB and RSI system
$ bash runModel.sh dow
we can change the index from dow to **sp500, nasdaq and other** which are included NYSE and others
