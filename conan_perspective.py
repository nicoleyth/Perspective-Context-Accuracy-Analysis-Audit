# --- imports ---
import csv
import pandas as pd
import time
import json
import requests

# --- Setup your Perspective API key here ---
API_KEY = 'AIzaSyCYJga0cfLWEdxcbc8Vq7O9eEt5XGVPWF8'

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# === Functions ===

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

# === Main ===

def main():
    # Load your DIALOCONAN CSV file
    df = pd.read_csv("DIALOCONAN.csv")  # <- Change to your path if needed
    
    # Only keep hate speech (HS) rows
    df = df[df['type'] == 'HS']

    # Output file
    output_file = 'perspective_scores_dialoconan.csv'

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['dialogue_id', 'turn_id', 'no_context_text', 'full_context_text', 'no_context_score', 'full_context_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each row
        for idx, row in df.iterrows():
            no_context_text = str(row['text'])
            dialogue_id = row['dialogue_id']
            turn_id = row['turn_id']

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
                'no_context_text': no_context_text,
                'full_context_text': full_context_input,
                'no_context_score': no_context_score,
                'full_context_score': full_context_score
            }
            writer.writerow(data)
            csvfile.flush()

    print("\n Analysis complete. Results saved to:", output_file)

# === Run the script ===

if __name__ == "__main__":
    main()
