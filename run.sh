#!/bin/sh
##echo "sp500" | python BolingerBands/BBEachTicker.py
python BolingerBands/BBEachTicker.py
python RelativeStrengthIndex/modelRSI.py
echo "selected" | python ChoiceTicker/StocksInfo.py
echo "selected" | python ChoiceTicker/StocksValue.py
