#!/bin/sh

DATA_DIR=../../data/sarc/

# GET_DATA.SH:
echo "Downloading and unpacking..."
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/train-balanced.csv.bz2 --save_file $DATA_DIR/train-balanced.csv.bz2
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/comments.json.bz2 --save_file $DATA_DIR/comments.json.bz2

bzip2 -df $DATA_DIR/train-balanced.csv.bz2
bzip2 -df $DATA_DIR/comments.json.bz2

# PARTITION_DEV.SH:
echo "Making dev set..."
python partition_dev.py --toy 0 --train $DATA_DIR/train-balanced.csv

# CSV_TO_JSON.SH:
echo "Converting to JSON..."
python csv_to_json.py --input $DATA_DIR/dev-balanced.csv --output $1

# create train JSON: (comment in if you intend to train your own model)
# python csv_to_json.py --input ../../data/sarc/train-no-dev-balanced.csv --output ../../data/sarc/train-no-dev-comments-balanced.json --dataset ../../data/sarc/comments.json

echo "Data preprocessing done!"
