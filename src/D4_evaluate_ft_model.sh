#!/bin/bash

# ADAPTED model:
FT_MODEL="dabagyan/sand-roberta-sarcasm-model"

# SARC dev
DATA_FILE="data/sarc/dev-comments-balanced.json"
FT_OUTPUT_FILE="outputs/D4/primary/devtest/d4_roberta_sand_model.out"
FT_RESULTS_FILE="results/D4/primary/devtest/D4_scores.out"

echo "Evaluating on SARC dev data..."
python -m src.model.evaluation $FT_MODEL $DATA_FILE $FT_OUTPUT_FILE $FT_RESULTS_FILE  --roberta --append_metrics

# SARC test
DATA_FILE="data/sarc/test-comments-balanced.json"
FT_OUTPUT_FILE="outputs/D4/primary/evaltest/d4_roberta_sand_model.out"
FT_RESULTS_FILE="results/D4/primary/evaltest/D4_scores.out"

echo "Evaluating on SARC test data..."
python -m src.model.evaluation $FT_MODEL $DATA_FILE $FT_OUTPUT_FILE $FT_RESULTS_FILE  --roberta --append_metrics

# SAND dev
DATA_FILE="data/scraped/dev.json"
FT_OUTPUT_FILE="outputs/D4/adaptation/devtest/d4_roberta_sand_model.out"
FT_RESULTS_FILE="results/D4/adaptation/devtest/D4_scores.out"

echo "Evaluating on SAND dev data..."
python -m src.model.evaluation $FT_MODEL $DATA_FILE $FT_OUTPUT_FILE $FT_RESULTS_FILE  --roberta --sand  --append_metrics

# SAND test
DATA_FILE="data/scraped/test.json"
FT_OUTPUT_FILE="outputs/D4/adaptation/evaltest/d4_roberta_sand_model.out"
FT_RESULTS_FILE="results/D4/adaptation/evaltest/D4_scores.out"

echo "Evaluating on SAND test data..."
python -m src.model.evaluation $FT_MODEL $DATA_FILE $FT_OUTPUT_FILE $FT_RESULTS_FILE  --roberta --sand --append_metrics

echo "Done!"
