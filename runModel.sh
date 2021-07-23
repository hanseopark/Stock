#!/bin/sh
HOME='pwd'
DATE=$(date '+%Y-%m-%d')
TRADE_DIR="data_ForTrading"
OUTPUT_DIR="${TRADE_DIR}/${DATE}"

if [ ! -d ${OUTPUT_DIR} ]
then
	mkdir -p ${OUTPUT_DIR}
fi

INDEX="$1"
OFFLINE="$2"

## To Get Stock's information
echo ${INDEX} | python ChoiceTicker/StocksValue.py

## To be explaind by ModelingIdea.md
## Like Swing Model
echo ${INDEX} | python BollingerBands/modelBB.py
echo ${INDEX} | python RelativeStrengthIndex/modelRSI.py

#echo "BB" | python RelativeStrengthIndex/modelRSI.py
#echo "selected" | python ChoiceTicker/StocksInfo.py
#echo "selected" | python ChoiceTicker/StocksValue.py
#python Strategy/AutoBackTesting.py

## To get stock
#echo "sp500" | python ChoiceTicker/StocksValue.py
#echo "sp500" | python ChoiceTicker/StocksInfo.py
#echo "sp500" | python ChoiceTicker/Preprocessing.py
