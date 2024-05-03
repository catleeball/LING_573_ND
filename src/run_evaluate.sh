#!/bin/bash


PROJECT_ROOT="$(pwd)"   # change if necessary, this works from D2.cmd
EVAL_DATA_FILE="$PROJECT_ROOT/data/sarc/dev-comments-balanced.json"
MODEL_NAME="Jade13/LING_573_ND_Trainer_D2_NoDev"
MODEL_OUTPUT_FILE="$PROJECT_ROOT/outputs/D2/d2.out"
METRICS_FILE="$PROJECT_ROOT/results/D2_scores.out"

# preprocess data
cd $PROJECT_ROOT/src/dev_partition/
./make_dev_set.sh $EVAL_DATA_FILE
cd $PROJECT_ROOT

# # run evaluation
# echo "Evaluating..."
# python -m src.model.evaluate $MODEL_NAME $EVAL_DATA_FILE $MODEL_OUTPUT_FILE $METRICS_FILE

