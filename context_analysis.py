"""
Authors: Kelli Eng & Nicole Huang
Date: 4/17/25
Description: This script converts collected toxicity scores into binary labels, calculates
toxicity score residuals, and runs evaluation metrics and visualizations.
"""
##### imports #####
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

##### main class #####
def main():
    # Load the Perspective API scores
    df = pd.read_csv("dataset/context_perspective_score.csv")

    # Rename for consistency
    df.rename(columns={"text_score": "toxicity_score"}, inplace=True)

    # Average toxicity score by label
    avg_scores = df.groupby('actual_score')['toxicity_score'].mean().reset_index()
    avg_scores['label_name'] = avg_scores['actual_score'].map({0: 'Non-Toxic', 1: 'Toxic'})
    print("\nAverage TOXICITY scores by label:")
    print(avg_scores[['label_name', 'toxicity_score']])

    # Plot score distributions
    plt.figure(figsize=(10, 6))
    for label in df['actual_score'].unique():
        subset = df[df['actual_score'] == label]['toxicity_score']
        label_name = 'Toxic' if label == 1 else 'Non-Toxic'
        plt.hist(subset, bins=20, alpha=0.5, label=label_name)
    plt.legend()
    plt.title("Toxicity Score Distribution by Human Label")
    plt.xlabel("Perspective API Score")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/context_toxicity_score_histogram.png")
    plt.show()
    plt.clf()

    df = pd.read_csv("dataset/context_perspective_score.csv")
    # Plot Actual Score vs Text Score
    plt.figure(figsize=(6, 6))
    plt.scatter(df['text_score'], df['parent_score'], alpha=0.6, color='blue', label='Text')
    plt.plot([0, 1], [0, 1], linestyle='--', color='orange', label='y = x')
    plt.xlabel("No Context API Toxicity Score")
    plt.ylabel("With Context API Toxicity Score")
    plt.title("No Context vs With Context Toxicity Score")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/context_no_contxt_vs_contxt.png")
    plt.show()
    plt.clf()

    # Apply threshold to parent_score for binary classification
    threshold = 0.33
    df['api_binary'] = df['parent_score'].apply(lambda x: 1 if x >= threshold else 0)
    print("\nUnique values in api_binary:", df['api_binary'].unique())

    # Confusion Matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(df['actual_score'], df['api_binary']))

    # False Positives and False Negatives
    false_positives = df[(df['actual_score'] == 0) & (df['api_binary'] == 1)]
    false_negatives = df[(df['actual_score'] == 1) & (df['api_binary'] == 0)]

    print(f"\nFalse Positives (Neutral tweets flagged as toxic): {len(false_positives)}")
    print(false_positives[['text', 'parent_score']].head(5))

    print(f"\nFalse Negatives (Toxic tweets missed by API): {len(false_negatives)}")
    print(false_negatives[['text', 'parent_score']].head(5))

    # Classification Performance
    print("\nLabel Distribution:")
    print(df['actual_score'].value_counts())

    print("\nClassification Report:")
    print(classification_report(df['actual_score'], df['api_binary'], target_names=["Non-Toxic", "Toxic"]))

    print("\nPrediction counts:")
    print(df['api_binary'].value_counts())

if __name__ == "__main__":
    main()
