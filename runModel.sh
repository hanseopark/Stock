#!/bin/sh
DATE=$(date '+%Y-%m-%d')
TRADE_DIR="data_ForTrading"
OUTPUT_DIR="${TRADE_DIR}/${DATE}"

if [ ! -d ${TRADE_DIR} ]
then
	mkdir -p ${TRADE_DIR}
fi

if [ ! -d ${OUTPUT_DIR} ]
then
	mkdir -p ${OUTPUT_DIR}
fi

INDEX="$1"

## To be explaind by ModelingIdea.md
## Like Swing Model
	# Bull or not
echo ${INDEX} | python Model/modelBull.py
OUTPUT=$( ( echo ${INDEX} | python Model/modelBull.py 2>&1 >/dev/null) )
echo ${OUTPUT}
	# Main
echo ${INDEX} | python Model/modelBB.py
echo ${INDEX} | python Model/modelHigh.py
echo ${INDEX} | python Model/modelRSI.py
	# Check Safety
echo ${INDEX} | python Model/CheckSafety.py

#python CombineDataFrame/CombineWithTicker.py

## Back Testing
#python Strategy/AutoBackTesting.py

