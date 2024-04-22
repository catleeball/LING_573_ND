#!/bin/sh
## create toy JSON:
python csv_to_json.py --input toy_train-balanced.csv --output toy_comments-train-balanced.json

# create dev JSON:
python csv_to_json.py --input ../../data/sarc/dev-balanced.csv --output ./../data/sarc/dev-comments-balanced.json