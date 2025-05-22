"""
Authors: Nicole Huang & Kelli Eng
Date: 4/3/25
Description: Analysis of Perspective toxicity data from pilot.py
"""
##### imports #####
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

##### main class #####
def main():
    # Load the CSV with original labels and Perspective API scores
    df = pd.read_csv("dataset/tweets_with_toxicity.csv")

    # Define class labels
    label_map = {0: 'Hate Speech', 1: 'Offensive', 2: 'Neither'}
    df['class_name'] = df['class'].map(label_map)

    # Combined toxicity (averaging hate_speech and offensive_language scores)
    df['combined_manual_score'] = (df['hate_speech'] + df['offensive_language']) / 10

    # Average toxicity score by class
    avg_scores = df.groupby('class_name')['toxicity_score'].mean().reset_index()
    print("\nAverage TOXICITY scores by label:")
    print(avg_scores)

    # Create gbinary label: 1 for Toxic (class 0 or 1), 0 for Non-Toxic (class 2)
    df['true_label'] = df['class'].apply(lambda x: 1 if x in [0, 1] else 0)

    # SGD to find best threshold
    best_thresh = 0.0
    best_score = 0.0

    for thresh in np.arange(0.0, 1.01, 0.01):
        df['pred_label'] = df['toxicity_score'].apply(lambda x: 1 if x >= thresh else 0)
        score = accuracy_score(df['true_label'], df['pred_label'])

        if score > best_score:
            best_score = score
            best_thresh = thresh

    print(f"Best threshold for toxicity_score: {best_thresh:.2f} with accuracy: {best_score:.4f}")

    # 2. Plot distribution of toxicity scores per class
    plt.figure(figsize=(10, 6))
    for label in df['class_name'].unique():
        subset = df[df['class_name'] == label]['toxicity_score']
        plt.hist(subset, bins=20, alpha=0.5, label=label)
    plt.legend()
    plt.title("Toxicity Score Distribution by Human Label")
    plt.ylabel("Frequency")
    plt.xlabel("Toxicity Score")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/pilot_toxicity_boxplot.png")

    # Scatter plot between combined toxicity vs toxicity score
    subset_df = df[df['class_name'].isin(['Offensive', 'Hate Speech', 'Neither'])]
    colors = {'Offensive': 'blue', 'Hate Speech': 'pink', 'Neither': 'green'}
    plt.figure(figsize=(10, 6))
    for label in ['Offensive', 'Hate Speech', 'Neither']:
        points = subset_df[subset_df['class_name'] == label]
        plt.scatter(points['combined_manual_score'], points['toxicity_score'],
                    color=colors[label], label=label, alpha=0.6, s=40)

    # Confusion-style analysis using the best threshold
    threshold = best_thresh
    df['api_pred'] = df['toxicity_score'].apply(lambda x: 'Toxic' if x >= threshold else 'Non-Toxic')

    # Define comment as toxic if class is 0 or 1
    df['true_label'] = df['class'].apply(lambda x: 'Toxic' if x in [0, 1] else 'Non-Toxic')

    plt.axhline(y=0.5, color='orange', linestyle='--', linewidth=2.0, label='Threshold = 0.5')
    plt.legend()
    plt.title("Toxicity Dataset Label vs API Toxicity Score")
    plt.xlabel("Given Dataset Label (hate_speech + offensive_language score)")
    plt.ylabel("Perspective API Toxicity Score")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/pilot_toxicity_combined_scatter.png")

    # Calculate mismatches
    confusion = pd.crosstab(df['true_label'], df['api_pred'], rownames=['Human Label'], colnames=['API Prediction'])
    print("\nConfusion Matrix:")
    print(confusion)

    # Output false positives and false negatives
    false_positives = df[(df['true_label'] == 'Non-Toxic') & (df['api_pred'] == 'Toxic')]
    false_negatives = df[(df['true_label'] == 'Toxic') & (df['api_pred'] == 'Non-Toxic')]

    print(f"\nFalse Positives (Neutral tweets flagged as toxic): {len(false_positives)}")
    print(false_positives[['tweet', 'toxicity_score']].head(5))

    print(f"\nFalse Negatives (Toxic tweets missed by API): {len(false_negatives)}")
    print(false_negatives[['tweet', 'toxicity_score']].head(5))

def count_distr(thresh, data):
    """
    Counts distribution of [neither, offensive, hate] count not in expected threshold range.
    (neither - below threshold line, offensive/hate - above threshold line)
    """
    results = []
    for label in ['Neither', 'Offensive', 'Hate Speech']:
        points = data[data['class_name'] == label]
        count = 0
        for _, p in points.iterrows():  # Iterate through each row in the subset
            if (label == 'Neither') & (p['toxicity_score'] < thresh):
                count += 1
            elif p['toxicity_score'] >= thresh:
                count += 1
        results.append(count)
    return results

if __name__ == "__main__":
    main()
