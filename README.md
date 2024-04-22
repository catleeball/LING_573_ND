# LING_573_ND

- Emails: emercha@uw.edu ; echm@uw.edu ; dabagyan@uw.edu ; jphore@uw.edu ; catball@uw.edu
- Notes doc: https://docs.google.com/document/d/1dRRhQ-tDifD92wgQnitI-MEr2HRGA1ejRvxnlqBdwmw/edit#heading=h.46l7ewibx4a2
- Drive: https://drive.google.com/drive/folders/1weS7nUDJJ_VrsxE2PJilDyicQqrfe65t
- Latex Report: https://www.overleaf.com/8838911828dkmzdmdsrjhh#6ca906

## Getting started
#### Installation
```
$ conda create -n 573_ND python=3.10 pip
$ conda activate 573_ND
$ pip install -r requirements.txt
```

#### Developer's notes
* The above installation ensures that you can do `pip install`, using the pip that comes natively within the conda environment. You can check by running `which pip`. 
* If you add more packages to the project, make sure to update the `requirements.txt`:
```
$ pip freeze > requirements.txt
```
* When running jupyter notebooks, make sure to set the kernel to the same python as the conda environment.

## Running the End-to-End System
After activating your conda environment with the proper requirements and system prerequisites, run the following commands. If you are not training your own model and want to evaluate our model, only run the Evaluation command. 
#### Data Pre-processing

#### Training 
$ python -m src.model.train_model

This training process will output training checkpoint directories to the outputs/models/ directory of the repo. Once training is finished, upload all files from the last checkpoint to Hugging Face on the Model Hub and ensure that your HF model repo is public. 

#### Evaluation
$ python -m src.model.evaluate

**The src/model/evaluate.py script in this repo evaluates our trained model and produces `outputs/D2/d2.out` and `results/D2_scores.out`. This is the only step you need to run if you are not re-training your own model.**
If running for your own model, note that the `model_name` variable must match the name of your Hugging Face Model Hub repo, beginning with your username. Ex: "Jade13/LING_573_ND_Trainer_D2_NoDev".

