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


