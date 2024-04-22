#!/bin/sh

# GET_DATA.SH:
# download and unpack 
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/train-balanced.csv.bz2 --save_file ../../data/sarc/train-balanced.csv.bz2
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/comments.json.bz2 --save_file ../../data/sarc/comments.json.bz2

bzip2 -df ../../data/sarc/train-balanced.csv.bz2
bzip2 -df ../../data/sarc/comments.json.bz2

# PARTITION_DEV.SH:
# make dev set
python partition_dev.py --toy 0 --train ../../data/sarc/train-balanced.csv

# CSV_TO_JSON.SH:
# create dev JSON:
python csv_to_json.py --input ../../data/sarc/dev-balanced.csv --output ../../data/sarc/dev-comments-balanced.json

# create train JSON: (comment in if you intend to train your own model)
# python csv_to_json.py --input ../../data/sarc/train-no-dev-balanced.csv --output ../../data/sarc/train-no-dev-comments-balanced.json --dataset ../../data/sarc/comments.json
