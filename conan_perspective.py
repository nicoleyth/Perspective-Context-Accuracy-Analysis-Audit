"""
Authors: Nicole Huang & Kelli Eng
Date: 4/25/25
Description: Collecting toxicity score from Perspective API using dialoconan dataset.

-----------

This file runs data through Google and Jigsaw's Perspective API, an open source API which 
measures the likely toxicity perception of the inputted text. (https://perspectiveapi.com/)

-----------

The dataset used for this project is from a Github repository titled "CONAN" by user 
'marcoguerini'. The repository is associated with the paper titled "Human-Machine 
Collaboration Approaches to Build a Dialogue Dataset for Hate Speech Countering" by 
Bonaldi, Dellantonio, Tekiroglu, and Guerin. Paper to appear in Proceedings of the 
2022 Conference on Empirical Methods in Natural Language Processing.

Link to Github repository here: https://github.com/marcoguerini/CONAN
Full dataset citation is located at the bottom of this page. 

Paper Citation: 
Helena Bonaldi, Sara Dellantonio, Serra Sinem Tekiroglu, and Marco Guerini. 2022. Human-Machine 
Collaboration Approaches to Build a Dialogue Dataset for Hate Speech Countering. 
arXiv preprint arXiv:2211.03433
"""
##### imports #####
import csv
import pandas as pd
import time
import json
import requests

# Perspective API key
API_KEY = 'AIzaSyCYJga0cfLWEdxcbc8Vq7O9eEt5XGVPWF8'

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

##### Functions #####

def get_context_text(dialogue_id, turn_id, df_all):
    """
    Get all earlier turns for the same dialogue.
    """
    dialogue_rows = df_all[(df_all['dialogue_id'] == dialogue_id) & (df_all['turn_id'] < turn_id)]
    context_texts = dialogue_rows['text'].tolist()
    return " ".join(context_texts)

def api_toxicity_score(text):
    """
    Send text to Perspective API and return the toxicity score.
    """
    time.sleep(1.5)  # Sleep to avoid rate limiting (max 60/minute)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    params = {
        'key': API_KEY
    }
    try:
        response = requests.post(PERSPECTIVE_URL, headers=headers, params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            score = result['attributeScores']['TOXICITY']['summaryScore']['value']
            return score
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception during API call: {e}")
        return None

##### Main Class #####

def main():
    # Load your DIALOCONAN CSV file
    df = pd.read_csv("dataset/DIALOCONAN.csv")
    
    # Only keep hate speech (HS) rows
    # df = df[df['type'] == 'HS']

    # Output file
    output_file = 'dataset/dialoconan_perspective_scores.csv'

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['dialogue_id', 'turn_id', 'type', 'no_context_score', 'full_context_score', 'no_context_text', 'full_context_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each row
        for idx, row in df.iterrows():
            no_context_text = str(row['text'])
            dialogue_id = row['dialogue_id']
            turn_id = row['turn_id']
            type = row['type']

            # Build full context
            context_text = get_context_text(dialogue_id, turn_id, df)
            full_context_input = context_text + " " + no_context_text if context_text else no_context_text

            # API calls
            print(f"Processing dialogue {dialogue_id}, turn {turn_id}...")
            no_context_score = api_toxicity_score(no_context_text)
            full_context_score = api_toxicity_score(full_context_input)

            # Write to file
            data = {
                'dialogue_id': dialogue_id,
                'turn_id': turn_id,
                'type': type,
                'no_context_score': no_context_score,
                'full_context_score': full_context_score,
                'no_context_text': no_context_text,
                'full_context_text': full_context_input
            }
            writer.writerow(data)
            csvfile.flush()

    print("\n Analysis complete. Results saved to:", output_file)

if __name__ == "__main__":
    main()

"""
@inproceedings{bonaldi-etal-2022-human,
    title = "Human-Machine Collaboration Approaches to Build a Dialogue Dataset for Hate Speech Countering",
    author = "Bonaldi, Helena  and
      Dellantonio, Sara  and
      Tekiroglu, Serra Sinem and
      Guerini, Marco",
    booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2022",
    publisher = "Association for Computational Linguistics",
    url = "https://preview.aclanthology.org/emnlp-22-ingestion/2022.emnlp-main.549/",
    pages = "8031--8049",
}
"""