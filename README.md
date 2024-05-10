# Data Dictionary Project

The script in this repository is a small example of the sort of plots and statistics that would be useful in a general purpose exploratory data analysis.

The `figures` directory contains some examples of plots that were produced for the online foods dataset.

# How to use

Replicate the development environment with

`conda env create -f environment.yml`

`conda activate ml_ds`

Run the main script

`python dict.py`

The program then asks for some options to be specified. The first is the dataset path which must be specified, e.g. `datasets/coffee.csv`.
Next are the target and date columns, which are optional.
To create the plots already in `figures/`, the options `datasets/vaccination_tweets.csv`, `user_verfied` and `date` were used.

# Acknowledgements & Licenses

The `vaccination_tweets.csv` data was released under an Apache 2.0 license and is available at https://www.kaggle.com/code/thomaskonstantin/pfizer-vaccine-sentiment-and-time-series-analysis/input

The `onlinefoods.csv` data was released under MIT license (Copyright (c) 2013 Mark Otto, Copyright (c) 2017 Andrew Fong.) and is available at https://www.kaggle.com/datasets/sudarshan24byte/online-food-dataset

The `coffee.csv` data was released under Apache 2.0 license and is avaiable at https://www.kaggle.com/datasets/keremkarayaz/coffee-shop-sales
