#!/bin/sh

DATA_DIR="data_origin"
PRE_DIR="data_preprocessing"

if [ ! -d ${DATA_DIR} ]
then
	mkdir -p ${DATA_DIR}
fi

if [ ! -d ${PRE_DIR} ]
then
	mkdir -p ${PRE_DIR}
fi

INDEX="$1"

echo ${INDEX} | python ChoiceTicker/StocksValue.py
echo ${INDEX} | python ChoiceTicker/StocksFS.py
echo ${INDEX} | python ChoiceTicker/StocksInfo.py
echo ${INDEX} | python Strategy/Preprocessing.py
