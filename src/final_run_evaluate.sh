#!/bin/sh
# NOTE: This script assumes you have the SARC and SAND datasets available in your data/ directory.

#--------------------------------------------------------------------------------------------------------------

# # BASE TRAINING ON D3 and D4 RoBERTa MODELS:
# # Comment in if SAND training predictions are not available.
# # SARC training predictions should be executed in a previous D4 .sh.

# # run from the main directory (LING_573_ND/)
# BASE_MODEL_1="dabagyan/roberta-sarcasm-model"
# BASE_OUTPUT_1="outputs/D4/roberta_sand_train_predictions.txt"
# BASE_MODEL_2="dabagyan/sand-roberta-sarcasm-model"
# BASE_OUTPUT_2="outputs/D4/sand_roberta_sand_train_predictions.txt"
# DATA_FILE="data/scraped/train.json"

# echo "Running D3 SARC-finetuned RoBERTA on SAND training set..."
# python -m src.model.evaluate_base_model $BASE_MODEL_1 $DATA_FILE $BASE_OUTPUT_1 --roberta --sand

# echo "Running D4 SAND-finetuned RoBERTA on SAND training set..."
# python -m src.model.evaluate_base_model $BASE_MODEL_2 $DATA_FILE $BASE_OUTPUT_2 --roberta --sand

#--------------------------------------------------------------------------------------------------------------

# TRAINING ON FINAL ENSEMBLE ON BOTH SAND AND SARC:

BASE_1_TRAIN_SARC="outputs/D4/roberta_sarc_train_predictions.txt"
BASE_1_TRAIN_SAND="outputs/D4/roberta_sand_train_predictions.txt"
BASE_2_TRAIN_SARC="outputs/D4/sand_roberta_sarc_train_predictions.txt"
BASE_2_TRAIN_SAND="outputs/D4/sand_roberta_sand_train_predictions.txt"
BASE_CONCAT_1="outputs/D4/roberta_cat_train_predictions.txt"
BASE_CONCAT_2="outputs/D4/sand_roberta_cat_train_predictions.txt"
SARC_TRAIN="data/sarc/train-no-dev-comments-balanced.json"
SAND_TRAIN="data/scraped/train.json"
LABEL_OUTPUT="outputs/D4/dual_train_labels.txt"
ENSEMBLE_FILE="outputs/D4/ensembles/dual_trained_roberta_ensemble_model.pkl"

# CONCATENATE - if concatenated data is not available, comment these in
# echo "Joining training set predictions..."
# python -m src.model.concat_training --load_preds $BASE_1_TRAIN_SARC $BASE_1_TRAIN_SAND --output_file $BASE_CONCAT_1
# python -m src.model.concat_training --load_preds $BASE_2_TRAIN_SARC $BASE_2_TRAIN_SAND --output_file $BASE_CONCAT_2

# echo "Joining training set true labels..."
# python -m src.model.concat_training --load_preds $SARC_TRAIN $SAND_TRAIN --data_to_label 0 1 --output_file $LABEL_OUTPUT

# TRAIN

# echo "Training model on all training sets..."
# python -m src.model.ensemble_model --train --load_preds $BASE_CONCAT_1 $BASE_CONCAT_2 --ensemble_file $ENSEMBLE_FILE --data_file $LABEL_OUTPUT --labels_only --max_depth 14 --criterion log_loss

# EVALUATE
# DEVTEST -------------------------------------

# SARC Dev Arguments
DATA_FILE="data/sarc/dev-comments-balanced.json"
BASE_OUTPUT_1="outputs/D4/primary/devtest/roberta_sarc_dev_predictions.txt"
BASE_OUTPUT_2="outputs/D4/primary/devtest/sand_roberta_sarc_dev_predictions.txt"
OUTPUT_FILE="outputs/D4/primary/devtest/d4_dual_trained_model.out"
RESULTS_FILE="results/D4/primary/devtest/D4_scores.out"

echo "SARC Dev Eval"
python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE

# SAND Dev Arguments
DATA_FILE="data/scraped/dev.json"
BASE_OUTPUT_1="outputs/D4/adaptation/devtest/roberta_sand_dev_predictions.txt"
BASE_OUTPUT_2="outputs/D4/adaptation/devtest/sand_roberta_sand_dev_predictions.txt"
OUTPUT_FILE="outputs/D4/adaptation/devtest/d4_dual_trained_model.out"
RESULTS_FILE="results/D4/adaptation/devtest/D4_scores.out"

echo "SAND Dev Eval"
python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE --sand

# EVALTEST -------------------------------------

# SARC Eval Arguments
DATA_FILE="data/sarc/test-comments-balanced.json"
BASE_OUTPUT_1="outputs/D4/primary/evaltest/roberta_sarc_test_predictions.txt"
BASE_OUTPUT_2="outputs/D4/primary/evaltest/sand_roberta_sarc_test_predictions.txt"
OUTPUT_FILE="outputs/D4/primary/evaltest/d4_dual_trained_model.out"
RESULTS_FILE="results/D4/primary/evaltest/D4_scores.out"

echo "SARC Test Eval"
python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE

# SAND Test Arguments
DATA_FILE="data/scraped/test.json"
BASE_OUTPUT_1="outputs/D4/adaptation/evaltest/roberta_sand_test_predictions.txt"
BASE_OUTPUT_2="outputs/D4/adaptation/evaltest/sand_roberta_sand_test_predictions.txt"
OUTPUT_FILE="outputs/D4/adaptation/evaltest/d4_dual_trained_model.out"
RESULTS_FILE="results/D4/adaptation/evaltest/D4_scores.out"

echo "SAND Test Eval"
python -m src.model.ensemble_model --data_file $DATA_FILE --load_preds $BASE_OUTPUT_1 $BASE_OUTPUT_2 --ensemble_file $ENSEMBLE_FILE --output_file $OUTPUT_FILE  --results_file $RESULTS_FILE --sand


