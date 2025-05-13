"""
Authors: Kelli Eng & Nicole Huang
Date: 4/16/25
Description: This file collects the toxicity score generated from Perspective API by Google
based on the text from the dataset in the datasets folder.

Warning: Processing the entire dataset takes 2 whole days (limitation to scores per hour). 
To save time, we've stored the collected toxicity scores from Perspective API in 
'perspective_score.csv' file.

-----------

This file runs data through Google and Jigsaw's Perspective API, an open source API which 
measures the likely toxicity perception of the inputted text. (https://perspectiveapi.com/)

-----------

The dataset used for this project is from a Github repository titled "context_toxicity" by
user 'ipavlopoulos'. The repository is associated with the paper titled "Toxicity Detection: 
Does Context Really Matter?" by Pavlopoulos, Sorenson, Dixon, et. al.

Link to Github repository here: https://github.com/ipavlopoulos/context_toxicity
Full dataset citation is located at the bottom of this page. 

Paper Citation: 
Pavlopoulos, J., Sorensen, J., Dixon, L., Thain, N., & Androutsopoulos, I. (2020). 
Toxicity Detection: Does Context Really Matter? ArXiv:2006.00998 [Cs].

"""
# --- imports ---
import csv
import pandas as pd
import time
import json
from googleapiclient import discovery

# --- Setup your Perspective API key here ---
API_KEY = 'AIzaSyCYJga0cfLWEdxcbc8Vq7O9eEt5XGVPWF8'

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

def main():
    # Load the dataset
    df = pd.read_csv("datasets/CAT_LARGE/gc.csv") 

    # Store toxicity scores here
    toxicity_scores = []
    toxicity_w_context = []

    with open('perspective_score.csv', 'w', newline='') as csvfile:
        fieldnames = ['text', 'parent_text','text_score','parent_score','actual_score','api_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.flush()


        # Analyze each tweet
        for i, row in df.iterrows():
            text = str(row['text']) #comment without context
            w_context = str(row['parent'] + row['text']) #comment with context
        
            tox_score = api_toxicity_gen(i, text)
            toxicity_scores.append(tox_score)
            tox_context_score = api_toxicity_gen(i, w_context)
            toxicity_w_context.append(tox_context_score)
            acc_score = int(row['label'])
            api_score = float(row['api'])

            data = {'text':text, 
                    'parent_text':w_context, 
                    'text_score':tox_score, 
                    'parent_score':tox_context_score, 
                    'actual_score':acc_score, 
                    'api_score': tox_score
                    }
            writer.writerow(data)
            csvfile.flush()
            time.sleep(1)  # Add delay for API rate limits

    # Add results to DataFrame and save 
    # df['toxicity_score'] = toxicity_scores
    # df.to_csv('tweets_with_toxicity.csv', index=False)
    print("\nAnalysis complete. Results saved to 'perspective_score.csv'")
    df = pd.read_csv("perspective_score.csv")
    print("\nScore Summary:")
    print(df['api_score'].describe())

def api_toxicity_gen(i, txt):
    """
    Function given text runs the toxicity api and returns toxicity score (0/1).
    """
    time.sleep(5)
    analyze_request = {
        'comment': {'text': txt},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']  # Force English to be used for now
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        print(f"[{i}] TOXICITY: {score:.3f} | Tweet: {txt[:50]}...")
        return score
    except Exception as e:
        print(f"[{i}] ERROR: {e}")
        return None
    
if __name__ == "__main__":
    main()

"""
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
"""