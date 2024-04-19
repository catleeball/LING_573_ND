from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import numpy as np
import json
import evaluate
from .utils import *
import torch

# Define the model name on Hugging Face
model_name = "Jade13/LING_573_ND_Trained_D2"

# Load the model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Define the path to your dev dataset
# project_root="~/LING_573_ND/"
project_root=""
data_dir = f"{project_root}data/sarc/"
test_filename = f"{data_dir}.json" # TODO: fill in filename

# Load the dev dataset
with open(test_filename) as f:
    test_data_raw = json.load(f)

# Preprocess the dev dataset
def preprocess_func(data, text_key="text"):
    return tokenizer(data[text_key], padding='max_length', truncation=True, max_length=512)

test_data = [{"text": d["response"], "label": int(d["label"])} for d in test_data_raw]
test_dataset = Dataset.from_list(test_data)
encoded_test_dataset = test_dataset.map(preprocess_func)
encoded_test_dataset = encoded_test_dataset.remove_columns('text')
encoded_test_dataset = encoded_test_dataset.with_format("torch")

#encoded_test_dataset = preprocess_data(test_data_raw, tokenizer)

# Define a function to compute metrics
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"f1": f1_metric.compute(predictions=predictions, references=labels)}

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

with open(f"{project_root}outputs/D2/d2.out", "w") as outputs:
    outputs.write(str(probabilities)) 

with open(f"{project_root}results/D2_scores.out", "w") as results:
    results.write(str(predictions.metrics))
