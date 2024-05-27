import json
import argparse
import torch
from transformers import Trainer, TrainingArguments
from .utils import *


parser = argparse.ArgumentParser(description='Evaluate a sarcasm detection model.')
# positional arguments
parser.add_argument('model_name', help='The name of the model on Huggingface, including the username/...')
parser.add_argument('test_filename', help='The name of the test dataset to evaluate the model on.')
parser.add_argument('model_output_file', help='The name of the file to print model predictions to.')
parser.add_argument('metrics_file', help='The name of the file to print model metrics (like f1) to.')
# boolean flags
parser.add_argument('--context', action='store_true', help='Include context comments when pre-processing evaluation data.')
parser.add_argument('--append_metrics', action='store_true', help='Append model metrics to metrics file instead of overwriting.')
parser.add_argument('--roberta', action='store_true', help='Whether the model uses ROBERTA or not (determines tokenizer).')
parser.add_argument('--sand', action='store_true', help='Whether input is SAND data (default is SARC).')

args = parser.parse_args()

# Load the model and tokenizer from Hugging Face
model, tokenizer = load_model(args.model_name, roberta=args.roberta)

# Load the dev dataset
with open(args.test_filename) as f:
    test_data_raw = json.load(f)

encoded_test_dataset = preprocess_data(test_data_raw, tokenizer, context=args.context, sand=args.sand)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",          # output directory
    per_device_eval_batch_size=64,   # batch size for evaluation
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # the instantiated hf Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    compute_metrics=compute_metrics,     # the callback that computes metrics of interest
    tokenizer=tokenizer,                 # used for autopadding
)

# Make predictions on the testing dataset
predictions = trainer.predict(test_dataset=encoded_test_dataset)

# Print the predictions
# Apply softmax to convert logits to probabilities
logits_tensor = torch.tensor(predictions.predictions)
probabilities = torch.softmax(logits_tensor, dim=1)

# Print the probabilities
# print(probabilities)
print(predictions.metrics)

with open(args.model_output_file, "w") as outputs:
    for p in range(0, len(probabilities)):
        true_label = encoded_test_dataset[p]["label"]
        prob_0 = float(probabilities[p][0])
        prob_1 = float(probabilities[p][1])
        if prob_0 < prob_1:
            pred = 1
        else:
            pred = 0
        outputs.write(f"pred: {pred}, gold: {true_label}, probs: {prob_0}, {prob_1}\n")

if args.append_metrics:
    write_mode = "a"
else:
    write_mode = "w"

with open(args.metrics_file, write_mode) as results:
    metrics = predictions.metrics
    results.write(f"Model: {args.model_name}\n")
    for m in metrics:
        results.write(f"{m}: {metrics[m]}\n")
    results.write("\n")
