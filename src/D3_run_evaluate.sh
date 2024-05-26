#!/bin/bash

PROJECT_ROOT="$(pwd)"   # change if necessary, this works from D3.cmd

# NOTE: if you do not have dev-comment-balanced.json, comment in partition lines (21-23)
EVAL_DATA_FILE="$PROJECT_ROOT/data/sarc/dev-comments-balanced.json"

# models to evaluate:
BASE_MODEL_NAME="dabagyan/bert-sarcasm-model"
BASE_MODEL_OUT_FILE="$PROJECT_ROOT/outputs/D3/d3_baseline.out"
ROBERTA_MODEL_NAME="dabagyan/roberta-sarcasm-model"
ROBERTA_MODEL_OUT_FILE="$PROJECT_ROOT/outputs/D3/d3_roberta.out"
CONT_MODEL_NAME="dabagyan/bert-context-sarcasm-model"
CONT_MODEL_OUT_FILE="$PROJECT_ROOT/outputs/D3/d3_context.out"
COMBINED_MODEL_NAME="dabagyan/roberta-context-sarcasm-model"
COMBINED_MODEL_OUT_FILE="$PROJECT_ROOT/outputs/D3/d3_combined.out"

METRICS_FILE="$PROJECT_ROOT/results/D3_scores.out"

# partition data - COMMENT OUT 3 LINES BELOW IF ALREADY DONE (in D2)
# cd $PROJECT_ROOT/src/dev_partition/
# ./make_dev_set.sh $EVAL_DATA_FILE
# cd $PROJECT_ROOT

# run evaluation on each model:
echo "Evaluating baseline..."
python -m src.model.evaluation $BASE_MODEL_NAME $EVAL_DATA_FILE $BASE_MODEL_OUT_FILE $METRICS_FILE

echo "Evaluating ROBERTA..."
python -m src.model.evaluation $ROBERTA_MODEL_NAME $EVAL_DATA_FILE $ROBERTA_MODEL_OUT_FILE $METRICS_FILE --append_metrics --roberta

echo "Evaluating with context..."
python -m src.model.evaluation $CONT_MODEL_NAME $EVAL_DATA_FILE $CONT_MODEL_OUT_FILE $METRICS_FILE --append_metrics --context

echo "Evaluating ROBERTA with context..."
python -m src.model.evaluation $COMBINED_MODEL_NAME $EVAL_DATA_FILE $COMBINED_MODEL_OUT_FILE $METRICS_FILE --append_metrics --context --roberta

