#!/bin/bash

BASE_MODEL_1="dabagyan/bert-sarcasm-model"
BASE_OUTPUT_1="outputs/D4/bert_sarc_dev_predictions.txt"
BASE_MODEL_2="dabagyan/roberta-sarcasm-model"
BASE_OUTPUT_2="outputs/D4/roberta_sarc_dev_predictions.txt"
DATA_FILE="data/sarc/dev-comments-balanced.json"
ENSEMBLE_FILE="outputs/D4/ensembles/sarc_no_context_ensemble_model.pkl"
OUTPUT_FILE="outputs/D4/d4_ensemble_sarc_d3_model.out"

# predict on evaluation data using base models
python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1
python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta

python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE
