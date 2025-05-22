*cite new dataset
# datasheet.md

## Motivation

This dataset (tweets_with_toxicity)was used for our audit on Perspective API's ability to detect toxic content in social media text. 
The goal was to compare the API's predicted `toxicity_score` to ground truth labels and explore its performance on various edge cases.

The data comes from Davidson et al.'s 2017 paper "Automated Hate Speech Detection and the Problem of Offensive Language". The task was to evaluate model fairness using metrics such as precision, recall, F1-score, and to identify issues such as false positives and false negatives in the API's predictions.

## Composition

Each row in the dataset contains:
- `text`: the main tweet being scored
- `parent_text`: context (optional, often the preceding message)
- `tox_codes_oc` / `tox_codes_ic`: multi-hot encoded vectors for outer and inner context annotations, such as identity attack, insult, etc.
- `label_oc` / `label_ic`: binary labels (0 = Non-Toxic, 1 = Toxic) based on annotations
- `toxicity_score`: a float score from the Perspective API (0.0 to 1.0)

We created a new column, `api_binary`, by thresholding `toxicity_score` at 0.5 to convert it into binary predictions (1 = toxic, 0 = non-toxic).

There are 7605 examples in total:
- 7481 labeled Non-Toxic
- 124 labeled Toxic

The dataset contains offensive language and is not filtered. No missing values were found in the key columns.

## Collection Process

The data was sourced from this GitHub repository:

> https://github.com/t-davidson/hate-speech-and-offensive-language/tree/master

It includes tweets labeled via crowdsourcing. The version used was the CSV format included in the `data/` directory of the repository. 
We added the Perspective API scores ourselves using a custom script (`analysis.py`) that sends each `text` entry to the API and saves the resulting `toxicity_score`.

No new data was collected or labeled. No direct identifiers (like names or user IDs) were included.

## Preprocessing / Cleaning / Labeling

Preprocessing steps:
- API scores were added using the Perspective API
- A binary column `api_binary` was created using a 0.5 threshold
- The `label_oc` column was used as the ground truth label for this lab

The script `analysis.py` automates this process and outputs classification metrics and examples of false positives and negatives. Raw and processed files were stored locally.

## Uses

Used in our project to:
- Audit the Perspective API for toxicity detection
- Examine confusion matrix results
- Identify trends in false positives and false negatives
- Reflect on bias and model limitations in content moderation systems

This dataset is useful for model evaluation and fairness auditing. However, it should not be used for deployment without deeper validation, given its sensitivity and labeling limitations.

## Distribution

Original dataset is public and hosted at:

> https://github.com/t-davidson/hate-speech-and-offensive-language/tree/master

Citation:

```bibtex
@inproceedings{offensivehatespeech,
  title = {Automated Hate Speech Detection and the Problem of Offensive Language},
  author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, 
  booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
  series = {ICWSM '17},
  year = {2017},
  location = {Montreal, Canada},
  pages = {512–515}
}

@inproceedings{hateoffensive,
  title = {Automated Hate Speech Detection and the Problem of Offensive Language},
  author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, 
  booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
  series = {ICWSM '17},
  year = {2017},
  location = {Montreal, Canada},
  pages = {512-515}
  }