import argparse
import json
import numpy as np
import random
import pickle
from pathlib import Path
from sklearn import tree
from sklearn.metrics import f1_score
from .utils import * # changed from relative import...

random.seed(13)

# Command line args
parser = argparse.ArgumentParser(description='Train an ensemble model for sarcasm detection.')
parser.add_argument('--train', action='store_true', help='Whether to train or evaluate the model. Evaluate by default.')
parser.add_argument('--data_file', type=str, help='The filename of the data the base models were fed.', required=True)
parser.add_argument('--load_preds', type=str, nargs='+', help='List of filenames for pre-existing base model outputs.', required=True)
parser.add_argument('--ensemble_file', type=str, help='Name of .pkl file to save the final decision tree to (or load from).', required=True)
parser.add_argument('--output_file', type=str, help="The file to output the ensemble's predictions to.")
parser.add_argument('--max_depth', type=int, default=None, help="The maximum depth of the decision tree.")
parser.add_argument('--criterion', type=str, default="gini", help="The function to measure quality of a split. (gini, entropy, log_loss)")
args = parser.parse_args()

# set data paths:
project_root = Path(__file__).cwd()
model_dir = project_root / "outputs"

# Load training labels:
print("Loading data...")
with open(args.data_file) as f:
    train_data_raw = json.load(f)
true_labels = np.array([int(d["label"]) for d in train_data_raw])

# Load base model predictions:
print("Loading existing base model predictions...")
prediction_arrays = []
for f in args.load_preds:
    # load base model predictions:
    predictions = np.loadtxt(f)
    prediction_arrays.append(predictions)

# concatenate predictions "sideways" (as features of the same instance)
ensemble_input = np.concatenate(prediction_arrays, axis=1)

if args.train:
    # train decision tree
    print("Training the ensemble model...")

    ensemble_clf = tree.DecisionTreeClassifier(max_depth=args.max_depth, 
                                            criterion=args.criterion)
    ensemble_clf = ensemble_clf.fit(ensemble_input, true_labels)

    # pickle decision tree
    print("Saving the ensemble model...")
    with open(args.ensemble_file, 'wb') as f:
        pickle.dump(ensemble_clf, f)

    print("Ensemble model saved.")
    
else:
    # evaluate decision tree
    print("Evaluating the ensemble model...")

    with open(args.ensemble_file, 'rb') as f:
        ensemble_clf = pickle.load(f)
    
    predictions = ensemble_clf.predict(ensemble_input)
    f1 = f1_score(y_true=true_labels, y_pred=predictions)
    print(f"F1 Score: {f1}")

    with open(args.output_file, "w") as f:
        for idx in range(len(true_labels)):
            pred = predictions[idx]
            gold = true_labels[idx]
            f.write(f"pred: {pred}, gold: {gold}\n")

    with open("results/D4_scores.out", "a") as f:
        f.write(f"Ensemble Filename: {args.ensemble_file}\n")
        f.write(f"Evaluation Data: {args.data_file}\n")
        f.write(f"\tF1 score: {f1}\n\n\n")