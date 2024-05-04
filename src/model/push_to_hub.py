import argparse
from transformers import BertForSequenceClassification, RobertaForSequenceClassification
from pathlib import Path

def dir_path(path):
    if Path(path).exists and Path(path).is_dir():
        return path
    else:
        raise NotADirectoryError(path)


parser = argparse.ArgumentParser(description='Push finetuned model to hub.')
parser.add_argument("-p", '--model-path', type=dir_path, help='Model Path to push to hub')
parser.add_argument("-n", '--model-name', type=str, help='Name for the model being pushed')
parser.add_argument('--roberta', action='store_true', help='Whether to use RoBERTa or BERT(default).')
args = parser.parse_args()

if args.roberta:
    model = RobertaForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=args.model_path,
    )
else:
    model = BertForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=args.model_path
    )

model.push_to_hub(
    args.model_name
)
