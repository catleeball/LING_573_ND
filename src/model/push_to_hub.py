import argparse

from transformers import BertForSequenceClassification

from pathlib import Path

def dir_path(path):
    if Path(path).exists and Path(path).is_dir():
        return path
    else:
        raise NotADirectoryError(path)


parser = argparse.ArgumentParser(description='Push finetuned model to hub.')
parser.add_argument("-p", '--model-path', type=dir_path, help='Model Path to push to hub')
parser.add_argument("-n", '--model-name', type=str, help='Name for the model being pushed')
args = parser.parse_args()

model = BertForSequenceClassification.from_pretrained(
    pretrained_model_name_or_path=args.model_path
)

model.push_to_hub(
    args.model_name
)