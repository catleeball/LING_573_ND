#!/bin/sh

# download and unpack 
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/train-balanced.csv.bz2 --save_file ../../data/sarc/train-balanced.csv.bz2
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/comments.json.bz2 --save_file ../../data/sarc/comments.json.bz2

bzip2 -df ../../data/sarc/train-balanced.csv.bz2
bzip2 -df ../../data/sarc/comments.json.bz2