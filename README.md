# Audit Project: Context Toxicity Analysis
Repository for the CS 266: AI & Society audit project.

For this project, we are auditing Google’s Perspective API, an AI-based tool used to detect harmful or toxic language in online content. The API assigns numerical scores to text based on attributes such as toxicity, insult, threat, and profanity, and is widely used by platforms to moderate user-generated content. Our focus is on evaluating how well the API identifies harmful content in real-world, informal language, particularly in cases where intent is difficult to detect—such as sarcasm, coded language, or internet slang. We are using a labeled dataset of tweets that includes examples of hate speech, offensive language, and neutral content. By comparing the API’s toxicity scores to these labels, we aim to understand how accurately and consistently it handles complex and ambiguous inputs.

We implemented our methodology on the following datasets. 

```bibtex
@inproceedings{chung-etal-2021-knowledge,
    title = "Towards Knowledge-Grounded Counter Narrative Generation for Hate Speech",
    author = "Chung, Yi-Ling and Tekiroğlu, Serra Sinem and Guerini, Marco",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics"
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

@inproceedings{offensivehatespeech,
  title = {Automated Hate Speech Detection and the Problem of Offensive Language},
  author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, 
  booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
  series = {ICWSM '17},
  year = {2017},
  location = {Montreal, Canada},
  pages = {512–515}
}

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