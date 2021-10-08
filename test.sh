#!/bin/bash

EX="$1"
OUTPUT=$(echo ${EX} | python test.py)
echo ${OUTPUT[1]}
