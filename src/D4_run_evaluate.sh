#!/bin/bash

<< '###'
NOTE: The inference time for our D3 models on the 4 datasets can be quite long. This
script processes them sequentially (not in parallel), so it will take... a while.
The predictions have already been saved to the repo under outputs/. If you would like
to run using these pre-loaded predictions, comment out the lines in the script below
where noted.
###

PROJECT_ROOT="$(pwd)"   # change if necessary, this works from D4.cmd

# ENSEMBLE model files:
BASE_MODEL_1="dabagyan/bert-sarcasm-model"
BASE_MODEL_2="dabagyan/roberta-sarcasm-model"
ENSEMBLE_FILE="outputs/D4/ensembles/sarc_no_context_ensemble_model.pkl"

# Retrieve SARC data:
cd $PROJECT_ROOT/src/dev_partition/
./make_dev_set.sh ../../data/sarc/dev-comments-balanced.json
./make_test_set.sh
cd $PROJECT_ROOT

# Retrieve SAND data (manually, in main README.md)

# # SARC Dev Set: -------------------------
# DATA_FILE="data/sarc/dev-comments-balanced.json"
# BASE_OUTPUT_1="outputs/D4/primary/devtest/bert_sarc_dev_predictions.txt"
# BASE_OUTPUT_2="outputs/D4/primary/devtest/roberta_sarc_dev_predictions.txt"
# OUTPUT_FILE="outputs/D4/primary/devtest/d4_ensemble_sarc_d3_model.out"
# RESULTS_FILE="results/D4/primary/devtest/D4_scores.out"

# # predict on evaluation data using base models
# # COMMENT OUT THE 2 LINES BELOW IF YOU WANT TO USE PRE-LOADED PREDICTIONS (saves a lot of time)
# python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1
# python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta

# python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE --results_file $RESULTS_FILE


# # SAND Dev Set: -------------------------
# DATA_FILE="data/scraped/dev.json"
# BASE_OUTPUT_1="outputs/D4/adaptation/devtest/bert_sand_dev_predictions.txt"
# BASE_OUTPUT_2="outputs/D4/adaptation/devtest/roberta_sand_dev_predictions.txt"
# OUTPUT_FILE="outputs/D4/adaptation/devtest/d4_ensemble_sarc_d3_model.out"
# RESULTS_FILE="results/D4/adaptation/devtest/D4_scores.out"

# # predict on evaluation data using base models
# # COMMENT OUT THE 2 LINES BELOW IF YOU WANT TO USE PRE-LOADED PREDICTIONS (saves a lot of time)
# python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1 --sand
# python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta --sand

# python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE --sand

# # #------------------------------------------------

# # SARC Eval Test Set: -------------------------
# DATA_FILE="data/sarc/test-comments-balanced.json"
# BASE_OUTPUT_1="outputs/D4/primary/evaltest/bert_sarc_test_predictions.txt"
# BASE_OUTPUT_2="outputs/D4/primary/evaltest/roberta_sarc_test_predictions.txt"
# OUTPUT_FILE="outputs/D4/primary/evaltest/d4_ensemble_sarc_d3_model.out"
# RESULTS_FILE="results/D4/primary/evaltest/D4_scores.out"

# # predict on evaluation data using base models
# # COMMENT OUT THE 2 LINES BELOW IF YOU WANT TO USE PRE-LOADED PREDICTIONS (saves a lot of time)
# python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1
# python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta

# python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE --results_file $RESULTS_FILE


# # SAND Eval Test Set: -------------------------
# DATA_FILE="data/scraped/test.json"
# BASE_OUTPUT_1="outputs/D4/adaptation/evaltest/bert_sand_test_predictions.txt"
# BASE_OUTPUT_2="outputs/D4/adaptation/evaltest/roberta_sand_test_predictions.txt"
# OUTPUT_FILE="outputs/D4/adaptation/evaltest/d4_ensemble_sarc_d3_model.out"
# RESULTS_FILE="results/D4/adaptation/evaltest/D4_scores.out"

# # predict on evaluation data using base models
# # COMMENT OUT THE 2 LINES BELOW IF YOU WANT TO USE PRE-LOADED PREDICTIONS (saves a lot of time)
# python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1 --sand
# python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta --sand

# python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE --sand