## Motivation

This dataset was used as part of our audit of the Perspective API, with a focus on evaluating the model's sensitivity to hate speech and counter-narratives in online dialogues. Our goal was to test whether the API’s toxicity scoring changes based on the inclusion of conversational context and how well it handles multi-turn interactions involving sensitive identity topics. The DIALOCONAN dataset offered a rare opportunity to evaluate model performance in dialogue rather than single-sentence analysis.

## Composition

Each row in the dataset represents a single turn in a multi-turn dialogue between a hate speech proponent and a counter-narrative responder. Fields include:

- `text`: the comment at a specific turn in the conversation
- `TARGET`: the group or identity being targeted (e.g., MIGRANTS, POC, LGBT+)
- `dialogue_id`: a unique identifier for each dialogue
- `turn_id`: the index of the turn within the dialogue
- `type`: whether the comment is hate speech (HS) or a counter-narrative (CN)
- `source`: the original collection source, such as "dialo_gold"

The dataset contains over 16,000 turns across 3,059 dialogues, with dialogues of length 4, 6, or 8 turns. Targets include JEWS, LGBT+, MIGRANTS, MUSLIMS, PEOPLE OF COLOR (POC), and WOMEN. Dialogues alternate between hateful and counter-responses and are synthetically constructed through human-machine collaboration.

## Collection Process

The DIALOCONAN dataset was constructed using a hybrid pipeline of machine-generated content and human expert post-editing. Specifically, the dialogues were generated using 19 different prompting strategies and then curated to reflect realistic online interactions. Each dialogue simulates a back-and-forth between an NGO operator and a user expressing hate speech.

Further details are documented in the original paper:

> Bonaldi, H., Dellantonio, S., Tekiroglu, S. S., & Guerini, M. (2022). Human-Machine Collaboration Approaches to Build a Dialogue Dataset for Hate Speech Countering. *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, pp. 8031–8049.

## Preprocessing / Cleaning / Labeling

- No additional labeling was added beyond the HS/CN classification provided in the original dataset.
- Some additional fields were appended in our analysis (e.g., Perspective API scores and toxicity classifications).
- All text entries were submitted to the Perspective API in both isolated and context-aware formats for evaluation.
- We introduced derived fields like toxicity score deltas and binary labels (e.g., toxic vs non-toxic) to simplify evaluation and visualize classification flips.

## Uses

Used in our project to:

- Evaluate how context affects Perspective API toxicity scores
- Compare API outputs between hate speech and counter-narratives
- Track classification shifts caused by added conversational context
- Highlight the challenges automated systems face in detecting intent in real-world dialogue

## Distribution

The DIALOCONAN dataset is publicly available and was created by Marco Guerini and collaborators. For more information, see the [CONAN GitHub repository](https://github.com/marcoguerini/CONAN).

### Citation

```bibtex
@inproceedings{chung-etal-2021-knowledge,
    title = "{Towards Knowledge-Grounded Counter Narrative Generation for Hate Speech",
    author = "Chung, Yi-Ling and Tekiroğlu, Serra Sinem and Guerini, Marco",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
}
}