"""
Authors: Nicole Huang & Kelli Eng
Date: 4/25/25
Description: Analysis of Perspective toxicity data collected from conan_perspective.py.
"""
##### imports #####
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression

##### main class #####
def main():
    #Load the results
    df = pd.read_csv("dataset/perspective_scores_dialoconan.csv")

    # Apply threshold to create binary labels
    threshold = 0.33
    df['no_context_binary'] = df['no_context_score'].apply(lambda x: 1 if x >= threshold else 0)
    df['full_context_binary'] = df['full_context_score'].apply(lambda x: 1 if x >= threshold else 0)

    # Confusion Matrix and Classification Report 
    print("\nConfusion Matrix: No Context vs Full Context")
    print(confusion_matrix(df['no_context_binary'], df['full_context_binary']))

    print("\nClassification Report: No Context vs Full Context")
    print(classification_report(df['no_context_binary'], df['full_context_binary'], target_names=['Non-Toxic', 'Toxic']))

    #Prediction counts 
    print("\nPrediction Counts:")
    print(df[['no_context_binary', 'full_context_binary']].value_counts())

    #dialogue averages 
    avg_scores = df.groupby('dialogue_id').agg({
        'no_context_score': 'mean',
        'full_context_score': 'mean'
    }).reset_index()

    #Scatter Plot with Dialogue Averages and Logistic Regression
    plt.figure(figsize=(8, 6))

    # Individual points (lighter, smaller)
    plt.scatter(df['no_context_score'], df['full_context_score'],
                alpha=0.15, s=10, label='Individual Comments', color='blue')

    # Dialogue averages (hollow orange X's)
    plt.scatter(avg_scores['no_context_score'], avg_scores['full_context_score'],
                facecolors='none', edgecolors='orange', marker='X', s=100, linewidths=2.5, label='Dialogue Averages')

    # Diagonal y=x line
    plt.plot([0, 1], [0, 1], linestyle='--', color='black', label='No Change Line (y = x)')

    plt.xlabel("Toxicity Score (No Context)", fontsize=12)
    plt.ylabel("Toxicity Score (With Context or Probability)", fontsize=12)
    plt.title("Toxicity Scores and Logistic Regression Fit (DIALOCONAN)", fontsize=14)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/conan_scatter_no_context_vs_full_context_logistic.png")
    plt.show()

    #Save DataFrame with binary labels into CSV file
    df.to_csv("dataset/conan_perspective_scores_dialoconan_binary.csv", index=False)

    # Plotting difference in toxicity score analysis
    df['score_delta'] = df['full_context_score'] - df['no_context_score']
    print("\nAverage score change due to context:", df['score_delta'].mean())
    print("Percent of comments that changed at all:", (df['score_delta'] != 0).mean() * 100, "%")
    print("Comments with increased score:", (df['score_delta'] > 0).sum())
    print("Comments with decreased score:", (df['score_delta'] < 0).sum())

    plt.figure(figsize=(7, 5))
    plt.hist(df['score_delta'], bins=40, color='skyblue', edgecolor='black')
    plt.axvline(0, color='black', linestyle='--')
    plt.title("Change in Toxicity Score (With Context - No Context)")
    plt.xlabel("Score Delta")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("figures/conan_scatter_no_context_vs_full_context.png")
    plt.show()

    # Count of the times that classification changed
    df['classification_changed'] = df['no_context_binary'] != df['full_context_binary']
    num_changed = df['classification_changed'].sum()
    print(f"\nNumber of comments whose classification flipped with context: {num_changed}")
    print("Percent of total:", round((num_changed / len(df)) * 100, 2), "%")

    # Save with binary predictions added to a new csv file
    df.to_csv("dataset/perspective_scores_dialoconan_binary.csv", index=False)

    # Extracting dialogues with most amount of turn_ids
    df = pd.read_csv("dataset/perspective_scores_dialoconan_binary.csv")

    # Get top 5 dialogues with most turns
    top_dialogues = (
        df.groupby('dialogue_id')['turn_id']
        .nunique()
        .sort_values(ascending=False)
        .head(6)
        .index
    )

    # Plotting pattern results
    for dialogue_id in top_dialogues:
        sub_df = df[df['dialogue_id'] == dialogue_id].sort_values('turn_id')

        plt.figure(figsize=(10,6))
        plt.scatter(sub_df['turn_id'], sub_df['no_context_score'], color='blue', alpha=0.7, s=100, label='No Context Score')
        plt.scatter(sub_df['turn_id'], sub_df['full_context_score'], color='orange', alpha=0.7, s=100, label='Full Context Score')

        plt.title(f"Dialogue ID {dialogue_id} - Compare Toxicity Scores by Turn")
        plt.xlabel("Turn ID")
        plt.ylabel("Toxicity Score")
        plt.ylim(0,1)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"figures/conan_progression_{dialogue_id}")

if __name__ == "__main__":
    main()
