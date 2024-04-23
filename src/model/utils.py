import numpy as np
import evaluate
from datasets import Dataset



def preprocess_data(raw_data, tokenizer):
    def preprocess_func(data, text_key="text"):
        return tokenizer(data[text_key], padding='max_length', truncation=True, max_length=512)

    data = [{"text": d["response"], "label": int(d["label"])} for d in raw_data]
    dataset = Dataset.from_list(data)

    encoded_dataset = dataset.map(preprocess_func)  

    encoded_dataset = encoded_dataset.remove_columns('text')    # training doesn't work if there are text columns
    return encoded_dataset.with_format("torch")


f1_metric = evaluate.load("f1")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return f1_metric.compute(predictions=predictions, references=labels)
