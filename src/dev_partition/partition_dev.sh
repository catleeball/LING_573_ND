#!/bin/sh

# make toy set
python partition_dev.py --toy 1 --train ../../data/sarc/train-balanced.csv
# make dev set
python partition_dev.py --toy 0 --train ../../data/sarc/train-balanced.csv