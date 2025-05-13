"""
Authors: Kelli Eng & Nicole Huang
Date: 4/17/25
Description: This file converts collected toxicity score into binary, calculates toxicity 
score residuals, and additional analysis based on aforementioned collected data. 
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

# --- Load the file with Perspective API scores ---
df = pd.read_csv("perspective_score.csv")

# --- Rename toxicity score column (optional for consistency) ---
df.rename(columns={"text_score": "toxicity_score"}, inplace=True)

# --- 1. Average Perspective API score by actual label ---
avg_scores = df.groupby('actual_score')['toxicity_score'].mean().reset_index()
avg_scores['label_name'] = avg_scores['actual_score'].map({0: 'Non-Toxic', 1: 'Toxic'})
print("\nAverage TOXICITY scores by label:")
print(avg_scores[['label_name', 'toxicity_score']])

# --- 2. Plot distribution of scores by actual label ---
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
plt.savefig("toxicity_score_histogram.png")
plt.show()

# --- 3. Apply threshold to make binary predictions (for evaluation only) ---
threshold = 0.3
df['api_binary'] = df['parent_score'].apply(lambda x: 1 if x >= threshold else 0)
print("\nUnique values in api_binary:", df['api_binary'].unique())

# --- 4. Confusion matrix ---
print("\nConfusion Matrix:")
print(confusion_matrix(df['actual_score'], df['api_binary']))

# --- 5. False positives and false negatives ---
false_positives = df[(df['actual_score'] == 0) & (df['api_binary'] == 1)]
false_negatives = df[(df['actual_score'] == 1) & (df['api_binary'] == 0)]

print(f"\nFalse Positives (Neutral tweets flagged as toxic): {len(false_positives)}")
print(false_positives[['text', 'parent_score']].head(5))

print(f"\nFalse Negatives (Toxic tweets missed by API): {len(false_negatives)}")
print(false_negatives[['text', 'parent_score']].head(5))

# --- 6. Label distribution and classification performance ---
print("\nLabel Distribution:")
print(df['actual_score'].value_counts())

print("\nClassification Report:")
print(classification_report(df['actual_score'], df['api_binary'], target_names=["Non-Toxic", "Toxic"]))

print("\nPrediction counts:")
print(df['api_binary'].value_counts())
