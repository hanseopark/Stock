#!/bin/sh
DOGET="$1"
DOMODEL="$2"

if [ "${DOGET}" = "y" ]
then
	echo "To get value, information with financial statements"
	for index in dow sp500 nasdaq other
	do
		bash runGET.sh $index
	done
	echo "Create All list add nasdaq and other"
	python CombineDataFrame/CreateAllTickerList.py
fi

if [ "${DOMODEL}" = "y" ]
then
	echo "To run model"
	for index in dow sp500 nasdaq other
	do
		bash runModel.sh $index
	done
	echo "Choice unique ticker"
	python CombineDataFrame/CombineWithTicker.py
fi


