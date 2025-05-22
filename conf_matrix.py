"""
Authors: Nicole Huang & Kelli Eng
Date: 4/5/25
Description: Created confusion matrix to analyze Perspective API toxicity score accuracy. 
"""
##### imports #####
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

##### main class #####
def main():
    # Load data
    df = pd.read_csv("perspective_score.csv")

    # Binary Perspective API scores at threshold 0.5
    df['predicted_label'] = (df['api_score'] >= 0.5).astype(int)

    # Compute confusion matrix
    cm = confusion_matrix(df['actual_score'], df['predicted_label'])

    # Set up labels
    labels = ['Non-Toxic', 'Toxic']

    # Create the heatmap
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)

    plt.xlabel('Predicted Label')
    plt.ylabel('Actual Label')
    plt.title('Perspective API: Confusion Matrix')
    plt.tight_layout()

    # Save and show the figure
    plt.savefig("perspective_conf_matrix.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
