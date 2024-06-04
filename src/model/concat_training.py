"""This script is used for the dually trained ensemble model. In order to train
on both the SARC and SAND training sets, the classifier needs to be fed both
predictions sets simultaneously--at least when using .fit().

Use this script from the root with:
    `python -m src.model.concat_training --load_preds <file1> <file2> ... 
    --output_file outputs/D4/<filepath>`
"""

import argparse
import numpy as np
import json

parser = argparse.ArgumentParser(description='Train an ensemble model for sarcasm detection.')
parser.add_argument('--load_preds', type=str, nargs='+', help='List of filenames containing predictions to concatenate.', required=True)
parser.add_argument('--data_to_label', type=int, nargs='*', help='Concatenate and output true labels (rather than predictions). List 0 for sarc format, 1 for sand, corresponding to order of load_preds.')
parser.add_argument('--output_file', type=str, help="The file to output the concatenated predictions to.", required=True)
args = parser.parse_args()

# Load base model predictions:
print("Loading existing base model predictions...")

if args.data_to_label:
    label_list = []
    print("Reading and concatenating labels...")
    for idx in range(len(args.load_preds)):
        filename = args.load_preds[idx]
        sand = args.data_to_label[idx]
        with open(filename) as f:
            data_raw = json.load(f)
        if sand:
            true_labels = [int(data_raw[d]["label"]) for d in data_raw]
        else:
            true_labels = [int(d["label"]) for d in data_raw]
        label_list = label_list + true_labels
    concat = np.array(label_list)

    print("Saving to output file...")
    np.savetxt(args.output_file, concat.astype(int))
    print("Predictions saved.")

# if we're outputting predicitons
else:
    prediction_arrays = []
    for filename in args.load_preds:
        # load base model predictions:
        predictions = np.loadtxt(filename)
        prediction_arrays.append(predictions)

    print("Concatenating predictions...")
    concat = np.concatenate(prediction_arrays, axis=0)

    print("Saving to output file...")
    np.savetxt(args.output_file, concat)
    print("Predictions saved.")
