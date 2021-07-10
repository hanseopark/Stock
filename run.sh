#!/bin/sh
#python BollingerBands/modelBB.py
#echo "BB" | python RelativeStrengthIndex/modelRSI.py
#echo "selected" | python ChoiceTicker/StocksInfo.py
#echo "selected" | python ChoiceTicker/StocksValue.py
#python Strategy/AutoBackTesting.py

echo "sp500" | python ChoiceTicker/StocksValue.py
echo "sp500" | python ChoiceTicker/StocksInfo.py
echo "sp500" | python Strategy/Preprocessing.py
