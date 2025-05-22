"""
Authors: Nicole Huang & Kelli Eng
Date: 4/3/25
Description: Collect API scoring data from harmful_language.csv

-----------

This file runs data through Google and Jigsaw's Perspective API, an open source API which 
measures the likely toxicity perception of the inputted text. (https://perspectiveapi.com/)

-----------

The dataset used for this project is from a Github repository titled "Hate Speech and Offensive 
Language Dataset" available on Kaggle, compiled by Andrii Samoshyn.

Link to Kaggle dataset here: https://www.kaggle.com/datasets/mrmorj/hate-speech-and-offensive-language-dataset
Full dataset citation is located at the bottom of this page. 

"""
##### imports #####
import pandas as pd
import time
import json
import os
from googleapiclient import discovery

##### main class #####
def main():
    # Perspective API key
    API_KEY = 'AIzaSyCYJga0cfLWEdxcbc8Vq7O9eEt5XGVPWF8'

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    # Load dataset
    df = pd.read_csv("dataset/harmful_language.csv")

    # Output CSV file setup
    output_file = 'tweets_with_toxicity.csv'
    if os.path.exists(output_file):
        os.remove(output_file)

    column_order = ['Unnamed: 0', 'count', 'hate_speech', 'offensive_language',
                    'neither', 'class', 'tweet', 'toxicity_score']

    # Iterate over each row and query the Perspective API
    for i, row in df.iterrows():
        text = str(row['tweet'])

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en']
        }

        try:
            response = client.comments().analyze(body=analyze_request).execute()
            score = response['attributeScores']['TOXICITY']['summaryScore']['value']
            print(f"[{i}] TOXICITY: {score:.3f} | Tweet: {text[:50]}...")
        except Exception as e:
            print(f"[{i}] ERROR: {e}")
            score = None

        row['toxicity_score'] = score

        # Write to CSV (header only on first write)
        row_df = pd.DataFrame([row])[column_order]
        if i == 0:
            row_df.to_csv(output_file, mode='w', header=True, index=False)
        else:
            row_df.to_csv(output_file, mode='a', header=False, index=False)

        time.sleep(1)

    print("\nAnalysis complete. Results saved to 'tweets_with_toxicity.csv'")

if __name__ == "__main__":
    main()

"""
@inproceedings{hateoffensive,
  title = {Automated Hate Speech Detection and the Problem of Offensive Language},
  author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, 
  booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
  series = {ICWSM '17},
  year = {2017},
  location = {Montreal, Canada},
  pages = {512-515}
  }
"""
