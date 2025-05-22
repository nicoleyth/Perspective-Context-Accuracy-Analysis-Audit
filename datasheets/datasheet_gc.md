# Dataset Card for GC Dataset (CAT-LARGE Subset, No Context)

## Motivation

This dataset was used in our audit of the Perspective API to evaluate its ability to detect toxic content in online conversations. The data includes paired dialogue turns from Wikipedia Talk Pages. Each entry consists of a comment (`text`) and the parent it is replying to (`parent`), along with a binary label (`label`) indicating whether the comment is toxic and a toxicity score (`api`) assigned by the Perspective API.

Our goal was to examine how well the API aligns with human-annotated labels and whether its predictions exhibit bias, misclassification, or context insensitivity. This is especially important when evaluating automated moderation tools, which are often used at scale.

## Task Description

- Task Type: Binary classification (Toxic vs. Non-Toxic)
- Evaluation Goal: Compare API predictions to human annotations
- Context Format: The API was evaluated on the reply (`text`) only; the `parent` was included for reference but not passed to the model.

## Dataset Details

- Source: Wikipedia Talk Pages
- Medium: Text-only
- Language: English
- Size: 10,000 comments
- Percentage Abusive: 0.6%
- Annotation Level: Post-level
- Annotation Type: Human-labeled toxicity (binary)
- Perspective API Version: v1alpha1 (TOXICITY attribute only)

## Composition

Each row in the dataset contains:

- `id`: A unique comment identifier
- `text`: The main comment analyzed by the Perspective API
- `parent`: The previous comment in the thread (context)
- `label`: Binary toxicity label (0 = Non-Toxic, 1 = Toxic)
- `api`: The API's toxicity score (float between 0.0 and 1.0)

The dataset consists of a wide range of Wikipedia discussions, including sarcastic, indirect, and ambiguous language.

## Collection Process

This dataset is based on the publicly available CAT-LARGE dataset from Pavlopoulos et al. (2020), specifically the no-context version. Human annotators labeled each comment independently of its parent. We submitted each `text` entry to the Perspective API and recorded the returned `TOXICITY` score.

Original data source:
> https://github.com/ipavlopoulos/context_toxicity

We did not alter the original labels or perform further manual annotation. The Perspective API scores were collected using a Python script that issued API calls and logged responses.

## Preprocessing / Labeling

- API scores (`api`) were added to the original dataset
- No additional cleaning, tokenization, or modification was applied
- Labels (`label`) were retained from the original dataset
- This file reflects a "no-context" setup; `parent` is included but unused by the API

## Uses

This dataset was used to:

- Compare Perspective API scores to gold-standard toxicity labels
- Identify false positives and false negatives
- Explore the effect of conversational ambiguity on toxicity predictions
- Provide baseline results for context-agnostic moderation systems

## Limitations

- All data is in English and may not generalize to other languages
- The dataset includes a relatively low proportion of toxic comments (~0.6%)
- Scores were obtained from an external system (Perspective API), not validated manually
- Context (`parent`) was not used in the model input, limiting insights into full-dialogue interpretation

## Distribution

- License: Public, for research use
- Data Link: https://github.com/ipavlopoulos/context_toxicity
- Publication: https://arxiv.org/pdf/2006.00998.pdf

## Citation

```bibtex
@inproceedings{xenos-etal-2021-context,
    title = "Context Sensitivity Estimation in Toxicity Detection",
    author = "Xenos, Alexandros  and
      Pavlopoulos, John  and
      Androutsopoulos, Ion",
    booktitle = "Proceedings of the 5th Workshop on Online Abuse and Harms (WOAH 2021)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.woah-1.15",
    doi = "10.18653/v1/2021.woah-1.15",
    pages = "140--145",
    abstract = "User posts whose perceived toxicity depends on the conversational context are rare in current toxicity detection datasets. Hence, toxicity detectors trained on current datasets will also disregard context, making the detection of context-sensitive toxicity a lot harder when it occurs. We constructed and publicly release a dataset of 10k posts with two kinds of toxicity labels per post, obtained from annotators who considered (i) both the current post and the previous one as context, or (ii) only the current post. We introduce a new task, context-sensitivity estimation, which aims to identify posts whose perceived toxicity changes if the context (previous post) is also considered. Using the new dataset, we show that systems can be developed for this task. Such systems could be used to enhance toxicity detection datasets with more context-dependent posts or to suggest when moderators should consider the parent posts, which may not always be necessary and may introduce additional costs.",
}
