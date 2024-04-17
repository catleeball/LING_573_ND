import numpy as np
import evaluate
import json
from datasets import Dataset
from transformers import AutoTokenizer, BertForSequenceClassification
from transformers import TrainingArguments, Trainer
from .utils import *


# project_root="~/LING_573_ND/"
project_root=""
data_dir = f"{project_root}data/sarc/"
model_dir = f"{project_root}outputs/models/"
train_filename = f"{data_dir}toy_comments-train-balanced.json"
eval_filename = f"{data_dir}dev-comments-balanced.json"


# LOAD MODEL
print("Loading model...")
pretrained_checkpoint = "google-bert/bert-base-uncased"     # switch to large later
id2label = {0: "not_sarcastic", 1: "sarcastic"} 

tokenizer = AutoTokenizer.from_pretrained(pretrained_checkpoint, use_fast=True)
model = BertForSequenceClassification.from_pretrained(pretrained_checkpoint, id2label=id2label)

# LOAD DATA
print("Loading data...")
with open(train_filename) as f:
    train_data_raw = json.load(f)
train_dataset = preprocess_data(train_data_raw, tokenizer)

with open(eval_filename) as f:
    eval_data_raw = json.load(f)
eval_dataset = preprocess_data(eval_data_raw[:10], tokenizer) 


# TRAIN MODEL
training_args = TrainingArguments(
    output_dir=model_dir,           # can do custom names
    evaluation_strategy = "epoch",
    save_strategy = "epoch",
    # push_to_hub=True,             # can push to hub instead of saving locally
    learning_rate=2e-5,             # defaults to Adam optimizer
    num_train_epochs=5,             # default is 3. BERT authors recommend 2-4
    logging_steps=1,                # to log loss from the first epoch
    load_best_model_at_end=True,
    metric_for_best_model="f1",     # default is loss
    # log_level="debug",            # default is warning
    logging_strategy="epoch",
)   


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# TRAIN
print("Beginning training...")
trainer.train()

# EVALUATE
print("Evaluating on dev set...")
print(trainer.evaluate())
print("Done!")
