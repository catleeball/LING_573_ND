# LING_573_ND

- Emails: emercha@uw.edu ; echm@uw.edu ; dabagyan@uw.edu ; jphore@uw.edu ; catball@uw.edu
- [Notes document](https://docs.google.com/document/d/1dRRhQ-tDifD92wgQnitI-MEr2HRGA1ejRvxnlqBdwmw/edit#heading=h.46l7ewibx4a2)
- [Google Drive](https://drive.google.com/drive/folders/1weS7nUDJJ_VrsxE2PJilDyicQqrfe65t)
- [Latex Report](https://www.overleaf.com/8838911828dkmzdmdsrjhh#6ca906)

### Models
- [dabagyan/bert-sarcasm-model](https://huggingface.co/dabagyan/bert-sarcasm-model)
- [dabagyan/bert-context-sarcasm-model](https://huggingface.co/dabagyan/bert-context-sarcasm-model)
- [dabagyan/roberta-sarcasm-model](https://huggingface.co/dabagyan/roberta-sarcasm-model)
- [dabagyan/roberta-context-sarcasm-model](https://huggingface.co/dabagyan/roberta-context-sarcasm-model)

## Getting started
#### Installation
```shell
$ conda create -n 573_ND python=3.10 pip
$ conda activate 573_ND
$ pip install -r requirements.txt
```

#### Developer's notes
* The above installation ensures that you can do `pip install`, using the pip that comes natively within the conda environment. You can check by running `which pip`. 
* If you add more packages to the project, make sure to update the `requirements.txt`:
```shell
$ pip list --format=freeze > requirements.txt
```
* When running jupyter notebooks, make sure to set the kernel to the same python as the conda environment.

## Running the system
After **activating your conda environment** with the proper requirements and system prerequisites, run the following commands. If you are not training your own model and want to evaluate our model, only run the Evaluation command. 

### Downloading SAND Data (Adaptation Task)
The SARC data is downloaded automatically in the evaluation script. However, the SAND data must be downloaded and placed in the `data/scraped/` directory manually. **Please download sand_data.tar.gz** from the following link: [https://huggingface.co/datasets/Jade13/SAND/tree/main](https://huggingface.co/datasets/Jade13/SAND/tree/main). Unzip it using the command below:
```shell
$ tar -xzf sand_data.tar.gz
```

Then place the files `dev.json` and `test.json` into the `data/scraped/` directory. They will be accessed with paths like: `data/scraped/dev.json`.

### Running end-to-end:
The following script runs the data preprocessing and model evaluation on SARC and SAND's dev and test sets, end-to-end, for our ensemble model, which uses the D3 fine-tuned BERT and RoBERTa (without context) as its base models. In other words, it runs 4 different evaluation sets. This is also the script used in `D4.cmd`.
```shell
$ src/D4_run_evaluate.sh
```

NOTE: Our `D4_run_evaluate.sh` script takes a long time to run, as it runs our model on all evaluation sets (dev and test). If you would like to run **just the evaluation set of the adaptation task**, comment out lines 26-70.

Furthermore, because the ensemble model takes predictions from 2 base models as input, our pre-saved base model predictions can be found under their respective folders in `outputs/`. There are comments in `D4_run_evaluate.sh` indicating what lines can be commented out to use these pre-saved predictions as input to the ensemble model.

### Running modularly:
#### Data Pre-processing
```shell
$ src/dev_partition/make_dev_set.sh
```
This script retrieves the relevant pieces of the SARC dataset, partitions the original training set into our training and dev sets, and converts the original .csv file into a JSON with the text and label data needed to run the model. *Comment in the last line of this file to also create the training JSON.*

#### Training 
##### BERT and RoBERTa:
```shell
$ python -m src.model.train_model [--context] [--roberta] [--push]
```
This training process will output training checkpoint directories to the `outputs/models/` directory of the repo. If `--push` is enabled, then the script automatically pushes the best model checkpoint to HuggingFace Hub. Make sure your `$HF_TOKEN` environment variable is set with your personal access token.

In case the model has to be pushed separately from training, the following command can be used:
```shell
$ python -m src.model.push_to_hub -p <insert/path/to/model> -n <insert-model-name>
```

For running training using docker-compose, 
```shell
$ docker-compose up -d train-context-model  # or other service name
```
##### Ensemble Model:
```shell
$ python -m src.model.evaluate_base_model <insert-model-name> <insert/path/to/data> <insert/path/to/predictions> [--roberta]
```
This command outputs the predictions of a base model to a file. Examples of these `.txt` files can be found in `outputs/D4/`. The datapath should point to your training data.

```shell
$ python -m src.model.ensemble_model --train --load_preds <insert/path/to/predictions_1> ... <.../predictions_n> --ensemble_file <insert/path/for/ensemble> --data_file <insert/path/to/data> [--max_depth] [--min_split] [--criterion]
```
This command takes multiple prediction files (each output by the previous command), concatenates the predictions, and uses them as input for an ensemble model. The optional flags `--max depth`, `--min_split`, and `--criterion` correspond to the arguments used when initializing the `DecisionTreeClassifier` from scikit-learn.


#### Evaluation
##### BERT and RoBERTa:
```shell
$ python -m src.model.evaluation <hf-model-name> <test-file> <model-output-file> <results-file>
```
The src/model/evaluate.py script in this repo evaluates our trained model and produces the files in `outputs/` and `results/`. If you have data to evaluate on (e.g., a dev or test set) and you are not re-training your own model, this is the only step you need to run.

There are additional flags available for use in src/model/evaluate.py:
- `--context` includes context comments when pre-processing the given `<test-file>`.
- `--append_metrics` opens the `<results-file>` in append mode, as opposed to overwriting the file contents.
- `--roberta` uses the pretrained RoBERTa tokenizer, as opposed to the BERT tokenizer.

These flags should match the loaded model; for example, if your `<hf-model-name>` is a fine-tuned RoBERTa model, you should use the `--roberta` flag. Examples of these flags are in `src/D3_run_evaluate.sh`.

If running for your own model, note that the `<hf-model-name>` argument must match the name of your Hugging Face Model Hub repo, beginning with your username. Ex: "Jade13/LING_573_ND_Trainer_D2_NoDev".

##### Ensemble Model:
```shell
$ python -m src.model.evaluate_base_model <insert-model-name> <insert/path/to/data> <insert/path/to/predictions> [--roberta] [--sand]
```
This command is similar to the training command. The datapath should point to your evaluation data. `--sand` should be used to indicate whether your evaluation data is SAND data. (By default, it is processed as SARC data.) Note that you can train on SAND data using this same flag, but it hasn't been fully tested.

```shell
$ python -m src.model.ensemble_model --load_preds <insert/path/to/predictions_1> ... <.../predictions_n> --ensemble_file <insert/path/to/ensemble> --data_file <insert/path/to/data> --output_file <insert/path/for/output> --results_file <insert/path/for/metrics> [--sand]
```
This command evaluates the performance of the ensemble model and appends the F1-score to a specified results file. Again, the `--sand` command should be used to indicate whether the evaluation data is SAND format.
