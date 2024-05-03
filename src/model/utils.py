import numpy as np
import evaluate
from datasets import Dataset


def preprocess_data(raw_data, tokenizer, context=False):
    def preprocess_func(data):
        return tokenizer(data["response"], truncation=True, max_length=512)
    
    # concatenate in reverse order, separated by special token
    def preprocess_func_context(data):
        # text = data['response'] + tokenizer.sep_token + data['posts'][-1]
        text = data['response']
        context = data['posts'][-1]
        return tokenizer(text, context, truncation=True, max_length=512)

    data = [{"response": d["response"], 
             "posts": d["posts"],
             "label": int(d["label"])} for d in raw_data]
    dataset = Dataset.from_list(data)

    encoded_dataset = dataset.map(preprocess_func_context) if context else dataset.map(preprocess_func)  

    encoded_dataset = encoded_dataset.remove_columns(['response', "posts"])    # training doesn't work if there are text columns
    return encoded_dataset.with_format("torch")


f1_metric = evaluate.load("f1")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return f1_metric.compute(predictions=predictions, references=labels)
