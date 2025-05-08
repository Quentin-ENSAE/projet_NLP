# Projet_NLP - Projet NLP — Multilingual Classification of Clinical Case Reports Using MeSH Categories

## 📑 Table of Contents

- [Project Objectives](#project-objectives)
- [Organisation of Notebooks](#organisation-of-notebooks)
- [Other Relevant Files](#-other-relevant-files)
- [References](#-references)

## Project objectives:
This project aims to automatically predict disease diagnoses using **Medical Subject Headings** (MeSH) categories from clinical case reports. The underlying dataset, derived from over 70,000 open-access and de-identified case reports, contains multimodal data including metadata, clinical narratives, demographic information (age, gender), and standardized diagnoses.

Our approach explores and compares classical NLP techniques and modern transformer-based models to address multi-label classification of disease categories (MeSH-C) on a corpus of more than 10,000 English clinical cases. We then augment the training data with synthetic clinical cases generated using Gemini and evaluate model performance on machine-translated French reports, thereby addressing multilingual classification challenges in low-resource settings.

## Organisation of Notebooks

### 📦 Preprocessing Notebooks

- **`Demo_dataset_creation`**  
  Demonstrates how to load and explore the MultiCaRe dataset.Notebook adapted from the [MultiCaRe GitHub repository](https://github.com/mauro-nievoff/MultiCaRe_Dataset.git). Illustrates how to load and perform an initial exploration of the MultiCaRe dataset.

- **`prétraitement`**  
  Merges the clinical case data with MeSH term annotations and applies multiple filters to extract the final dataset of 10,000 English clinical cases, split into training (8,574), validation (1,072), and test (1,072) sets.

- **`Encoding_MeSH_terms`**  
  Maps MeSH descriptors to their corresponding high-level chapter categories (C01–C26) to facilitate multi-label classification at the MeSH-C level.

### 📊 Analysis Notebooks

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

### 📁 Other Relevant Files

- **Rapport_Mini Projet NLP_Quentin MARRET.pdf**
  Final report presenting the full methodology, experimental setup, and analysis of results.

- **`Script`**  
  Contains Python scripts with all core functions for feature engineering and MeSH preprocessing (e.g., mapping MeSH terms to target labels for classification).
  
- **`GEMINI`**  
  Includes the prompt used to generate synthetic French clinical cases with Gemini.

- **`data/`**  
  Contains preprocessed train and test datasets used in all model training pipelines.

### 📚 References

MeSH Classification Tree
The full MeSH hierarchical structure is available in .xml format from the U.S. National Library of Medicine.
🔗 Download desc2025.xml



- MeSH Classification Tree
The full MeSH hierarchical structure is available in .xml format from the U.S. National Library of Medicine.
🔗 [Download desc2025.xml](https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2025.xml)

- MultiCaRe Dataset
A multimodal dataset of 75,000+ clinical case reports including metadata, images, and MeSH annotations.
🔗 [Zenodo Record](https://zenodo.org/records/14994046)

- Dataset Description Paper
Dataset of clinical cases, images, image labels and captions from open access case reports from PubMed Central (1990–2023)
Data in Brief, 2024
🔗 [Read on ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352340923010351?via%3Dihub)

- Reference Scientific Paper
Multilabel classification of medical concepts for patient clinical profile identification — includes benchmark methods and multilingual evaluation.
Artificial Intelligence in Medicine, 2022
🔗 [Read on ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0933365722000768?via%3Dihub)


### 📚 References

- **MeSH Classification Tree**  
  The full MeSH hierarchical structure is available in `.xml` format from the U.S. National Library of Medicine.  
  🔗 [Download desc2025.xml](https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2025.xml)

- **MultiCaRe Dataset**  
  A multimodal dataset of 75,000+ clinical case reports including metadata, images, and MeSH annotations.  
  🔗 [Zenodo Record](https://zenodo.org/records/14994046)

- **Dataset Description Paper**  
  *Dataset of clinical cases, images, image labels and captions from open access case reports from PubMed Central (1990–2023).*  
  _Data in Brief, 2024_  
  🔗 [Read on ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352340923010351?via%3Dihub)

- **Reference Scientific Paper**  
  *Multilabel classification of medical concepts for patient clinical profile identification* — includes benchmark methods and multilingual evaluation.  
  _Artificial Intelligence in Medicine, 2022_  
  🔗 [Read on ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0933365722000768?via%3Dihub)
