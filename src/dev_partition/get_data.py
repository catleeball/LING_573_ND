
from urllib.request import urlretrieve
import argparse

if __name__ == "__main__":

    default_url = "https://nlp.cs.princeton.edu/old/SARC/2.0/main/train-balanced.csv.bz2"
    default_filename = "../../data/sarc/train-balanced.csv.bz2"

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default=default_url, help="Enter the URL (ending in the filename) to download the file from.")
    parser.add_argument("--save_file", type=str, default=default_filename, help="Enter the filename to save the downloaded file to.")

    args = parser.parse_args()

    path, headers = urlretrieve(args.url, args.save_file)
