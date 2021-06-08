#!/bin/sh
#echo "sp500" | python BolingerBands/BBEachTicker.py
python BolingerBands/BBEachTicker.py
python RelativeStrengthIndex/modelRSI.py
