#!/bin/sh

DATA_DIR=../../data/sarc/

# GET_DATA.SH:
echo "Downloading and unpacking..."
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/test-balanced.csv.bz2 --save_file $DATA_DIR/test-balanced.csv.bz2
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/comments.json.bz2 --save_file $DATA_DIR/comments.json.bz2

bzip2 -df $DATA_DIR/test-balanced.csv.bz2
bzip2 -df $DATA_DIR/comments.json.bz2

# CSV_TO_JSON.SH:
echo "Converting to JSON..."
python csv_to_json.py --input $DATA_DIR/test-balanced.csv --output $DATA_DIR/test-comments-balanced.json

echo "Data preprocessing done!"