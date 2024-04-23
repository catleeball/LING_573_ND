import json
import sys
import torch
from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from .utils import *


# Define the model name on Hugging Face
# model_name = "Jade13/LING_573_ND_Trainer_D2_NoDev"
model_name = sys.argv[1]
test_filename = sys.argv[2]
model_output_file = sys.argv[3]
metrics_file = sys.argv[4]

# Load the model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Define the path to your dev dataset
# project_root=""
# data_dir = f"{project_root}data/sarc/"
# test_filename = f"{data_dir}/dev-comments-balanced.json" # TODO: fill in filename
# model_output_file = f"{project_root}outputs/D2/d2.out"
# metrics_file = f"{project_root}results/D2_scores.out"

# Load the dev dataset
with open(test_filename) as f:
    test_data_raw = json.load(f)

encoded_test_dataset = preprocess_data(test_data_raw, tokenizer)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",          # output directory
    per_device_eval_batch_size=64,  # batch size for evaluation
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # the instantiated hf Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    compute_metrics=compute_metrics,     # the callback that computes metrics of interest
)

# Make predictions on the testing dataset
predictions = trainer.predict(test_dataset=encoded_test_dataset)

# Print the predictions
# Apply softmax to convert logits to probabilities
logits_tensor = torch.tensor(predictions.predictions)
probabilities = torch.softmax(logits_tensor, dim=1)

# Print the probabilities
print(probabilities)
print(predictions.metrics)

with open(model_output_file, "w") as outputs:
    outputs.write(str(probabilities)) 

with open(metrics_file, "w") as results:
    results.write(str(predictions.metrics))
