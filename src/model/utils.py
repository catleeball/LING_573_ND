import numpy as np
import evaluate
from datasets import Dataset
from transformers import AutoTokenizer, BertForSequenceClassification
from transformers import RobertaForSequenceClassification


def load_model(model_checkpoint, roberta=False):
    id2label = {0: "not_sarcastic", 1: "sarcastic"} 

    tokenizer_name = "roberta-base" if roberta else "google-bert/bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=True)

    if roberta:
        model = RobertaForSequenceClassification.from_pretrained(model_checkpoint, id2label=id2label)
    else: 
        model = BertForSequenceClassification.from_pretrained(model_checkpoint, id2label=id2label)
    return model, tokenizer


def preprocess_data(raw_data, tokenizer, context=False, sand=False):
    def preprocess_func(data):
        return tokenizer(data["text"], truncation=True, max_length=512)
    
    # concatenate in reverse order, separated by special token
    def preprocess_func_context(data):
        # text = data['response'] + tokenizer.sep_token + data['posts'][-1]
        text = data['text']
        context = data['posts'][-1]
        return tokenizer(text, context, truncation=True, max_length=512)

    if sand:
        data = list(raw_data.values())
    else:
        data = [{"text": d["response"], 
                "posts": d["posts"],
                "label": int(d["label"])} for d in raw_data]
    
    dataset = Dataset.from_list(data)
    encoded_dataset = dataset.map(preprocess_func_context) if context else dataset.map(preprocess_func)  

    # training doesn't work if there are text columns
    if "token_type_ids" in encoded_dataset.column_names:
        encoded_dataset = encoded_dataset.select_columns(['input_ids', "token_type_ids", "attention_mask", "label"])  
    else:
        encoded_dataset = encoded_dataset.select_columns(['input_ids', "attention_mask", "label"])    
    return encoded_dataset.with_format("torch")


f1_metric = evaluate.load("f1")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return f1_metric.compute(predictions=predictions, references=labels)
