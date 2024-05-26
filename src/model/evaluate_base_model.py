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
# boolean flags
parser.add_argument('--context', action='store_true', help='Include context comments when pre-processing evaluation data.')
parser.add_argument('--roberta', action='store_true', help='Whether the model uses ROBERTA or not (determines tokenizer).')

args = parser.parse_args()

# Load the model and tokenizer from Hugging Face
model, tokenizer = load_model(args.model_name, roberta=args.roberta)

# Load the dev dataset
with open(args.test_filename) as f:
    test_data_raw = json.load(f)

encoded_test_dataset = preprocess_data(test_data_raw, tokenizer, context=args.context)

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
np.savetxt(args.model_output_file, predictions.predictions)

