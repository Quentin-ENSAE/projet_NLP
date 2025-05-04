# projet_NLP
Git pour le projet du cours de machine learning for NLP.

# Project objectives:
I will use a medical dataset containing multi-modal data from over 70,000 open access and de-identified case reports, including metadata, clinical cases, demographic data (gender, age) and diagnosis using MeSH standard. 

The objective of my (mini) project is to etrieve demographic data (gender, age) and to predict diagnosis in MeSH standards using different NLP methods/models. 

# Clinical Case Classification - NLP Project

## 📦 Preprocessing Notebooks

- **`Demo_dataset_creation`**  
  Notebook taken from the [MultiCaRe GitHub repository](https://github.com/mauro-nievoff/MultiCaRe_Dataset.git). Demonstrates how to load and explore the MultiCaRe dataset.

- **`prétraitement`**  
  Merges the dataset of clinical cases with MeSH term annotations and applies various filters to extract the 10,000 final clinical cases used for training.

- **`Encoding_MeSH_terms`**  
  Encodes MeSH terms into broader chapter-level categories (C01–C26).

## 📊 Analysis Notebooks

- **`Analyse_descriptive`**  
  Performs descriptive analysis on the filtered dataset.

- **`Naives_classifier_en`**  
  Trains a One-VS-Rest classifier on English clinical cases.

- **`Naives_classifier_fr`**  
  Trains a One-VS-Rest classifier on synthetic French clinical cases.

- **`BioBERT_Training`**  
  Trains the BioBERT model on the English dataset.

- **`BERT-base-multilingual`**  
  Trains the multilingual BERT model on both English and French datasets.

- **`BERT-base-multilingual_EN`**  
  Trains the multilingual BERT model on English only to assess its zero-shot performance on French test cases.

- **`Training_Dilution`**  
  Queries the Gemini 2.0 Flash model to generate synthetic French clinical cases.

- **`Translation`**  
  Selects English clinical cases from the test set and translates them into French for use as a French test set.

## 📁 Other Relevant Files

- **`Script`**  
  Contains two Python files with all the core functions used in feature engineering and MeSH preprocessing (e.g., converting MeSH terms to model targets).

- **`GEMINI`**  
  Includes the prompt used to generate synthetic French clinical cases with Gemini.

- **`data/`**  
  Contains preprocessed train and test datasets used in all model training pipelines.

## 🌲 MeSH Classification Tree

The full MeSH classification tree is available in `.xml` format from the National Library of Medicine:  
🔗 [https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/](https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/)



## Références: 
**Dataset URL** : https://zenodo.org/records/14994046 
**Data paper about dataset creation** : https://www.sciencedirect.com/science/article/pii/S2352340923010351?via%3Dihub
**Scientific paper using Instruct GPT3 to retrive information from medical case reports** : https://www.sciencedirect.com/science/article/pii/S0169260724003195
