# download and unpack 
# make toy set
python partition_dev.py --toy 1 --train train-balanced.csv
# make dev set
python partition_dev.py --toy 0 --train train-balanced.csv