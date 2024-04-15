# This script retrieves the lines from the training file.
# If the --toy flag is specified as 0, 10% of the training
# data will be randomly selected (alongside the first 10 lines).
# If the --toy flag is 1, the first 10 lines of the training
# data is returned.

import argparse
import random
import math

if __name__ == "__main__":

    # set seed so dev set is always the same
    random.seed(573)

    # command line arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toy", type=int, default=0, help="Select which dev set size to create: 0 = full dev set, 1 = toy set.")
    parser.add_argument("--train", type=str, default="train-balanced.csv", help="The training set to take 10% (or the first 10 items if toy) from.")
    args = parser.parse_args()

    # specfiy output filename based on --toy flag
    if args.toy:
        out_filename = "toy_train-balanced.csv"
    else:
        out_filename = "dev-balanced.csv"

    # select lines from training file & output to partition file
    with open(args.train, "r") as train_file:
        with open(out_filename, "w") as dev_file:

            # store training instance lines & length of training file
            train_lines = train_file.readlines()
            train_len = len(train_lines)

            # the number of lines to randomly select (in addition to first 10 lines)
            random_size = math.floor((train_len-100) * 0.10)

            # make a list of indices to sample from the training file
            partition_indices = list(range(1, 11))
            if args.toy == 0:
                partition_indices.extend(random.sample(range(11, train_len+1), random_size))
            
            # loop through training lines & write sample lines to dev file
            line_num = 1
            for line in train_lines:
                # check if current line should be sampled
                if line_num in partition_indices:
                    dev_file.write(line)
                line_num += 1
                # end loop early if only making toy set
                if args.toy and line_num > 10:
                    break