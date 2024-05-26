import json
import argparse
import torch
from transformers import AutoTokenizer, BertForSequenceClassification
from transformers import RobertaForSequenceClassification
from transformers import TrainingArguments, Trainer
from pathlib import Path
from .utils import *


parser = argparse.ArgumentParser(description='Finetune BERT model for sarcasm detection.')
parser.add_argument('--context', action='store_true', help='Whether or not to use post context.')
parser.add_argument('--roberta', action='store_true', help='Whether to use RoBERTa or BERT(default).')
parser.add_argument('--push', action='store_true', help='Push final model to HuggingFace Hub.')
parser.add_argument('--sand', action='store_true', help='Whether to use SAND data (default is SARC).')
args = parser.parse_args()

model_id = f'{"roberta-" if args.roberta else "bert-"}{"context-" if args.context else ""}sarcasm-model'
data_mode = "sand" if args.sand else "sarc"

project_root = Path(__file__).cwd()
data_dir = project_root / "data" / data_mode
model_dir = project_root / "outputs" / model_id
# train_filename = data_dir / "train-no-dev-comments-balanced.json"
# eval_filename = data_dir / "dev-comments-balanced.json"
train_filename = data_dir / "train.json"
eval_filename = data_dir / "dev.json"


# LOAD MODEL
print("Loading model...")
# pretrained_checkpoint = "roberta-base" if args.roberta else "google-bert/bert-base-uncased" 
pretrained_checkpoint = "dabagyan/roberta-sarcasm-model"
model, tokenizer = load_model(pretrained_checkpoint, roberta=args.roberta)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Training model using device: {device}")
print(f"Training model id: {model_id}")
print(f"Using pretrained: {pretrained_checkpoint}")


# LOAD DATA
print("Loading data...")
with open(train_filename) as f:
    train_data_raw = json.load(f)
if args.sand:   
    train_dataset = preprocess_data_sand(train_data_raw, tokenizer)
else:
    train_dataset = preprocess_data_sarc(train_data_raw, tokenizer, context=args.context)

with open(eval_filename) as f:
    eval_data_raw = json.load(f)
if args.sand:
    eval_dataset = preprocess_data_sand(eval_data_raw, tokenizer) 
else:
    eval_dataset = preprocess_data_sarc(eval_data_raw, tokenizer, context=args.context) 


# TRAIN MODEL
training_args = TrainingArguments(
    output_dir=model_dir,          
    evaluation_strategy = "epoch",
    save_strategy = "epoch",
    learning_rate=2e-5,             # defaults to Adam optimizer
    num_train_epochs=4,             # default is 3. BERT authors recommend 2-4
    logging_steps=1,                # to log loss from the first epoch
    load_best_model_at_end=True,
    metric_for_best_model="eval_f1",# default is loss
    log_level="debug",              # default is warning
    logging_strategy="epoch",
)  

if args.push:
    training_args.set_push_to_hub(model_id, strategy="end")

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
