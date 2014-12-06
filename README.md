# Actively Detecting Social Bots: Twitter Case
====
## CS579 Project: Online Social Network Analysis

Social media is a popular outlet to let message reach a vast number of people. It has also become an important source of revenue for those with significant online presence. However, a big issue is to determine how real is that presence. It is easy create a fake audience or even purchase it, mainly due to the lack of verification procedures. Machine learning methods have shown to be effective to identify unmanned account. However, automation methods also evolve to avoid detection and force learned models to be updated. We propose an anytime active learning method to gather labeled data and train a model more effiently.  

## Content
This repository is organized as follows: 
* Notebooks
* Presentations
* Report 
* src

### Notebooks
This folder contains **data_process.ipynb** notebook which defines functions to load and preprocess the tweeter collected data. It includes the results used for analysis. 

### Presentations
Contains the proposal and project presentation

### Report
Containt the report files. The main file is **master.pdf** ([see here](https://github.com/mramire8/osna/blob/master/report/master.pdf)).

##src
This folder contains the code needed to collect the data. The main files are:

1. ```data_collect.py``` this file contains the code to collect the timeline of users from Twitter. We used 1000 user from each kind good and bot. 
2. ```active learning``` active learning code is located at the [active learning](https://github.com/mramire8/active) repository

After using ```data_collect```, the data can be used as dataset using the function describe in the notebook. 
