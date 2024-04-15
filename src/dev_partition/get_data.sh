# download and unpack 
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/train-balanced.csv.bz2 --save_file train-balanced.csv.bz2
python get_data.py --url https://nlp.cs.princeton.edu/old/SARC/2.0/main/comments.json.bz2 --save_file comments.json.bz2

bzip2 -df train-balanced.csv.bz2
bzip2 -df comments.json.bz2