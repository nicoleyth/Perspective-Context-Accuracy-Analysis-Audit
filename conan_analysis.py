# --- imports ---
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# --- Load the results ---
df = pd.read_csv("csv/perspective_scores_dialoconan.csv")

# --- 1. Binarize the Perspective scores ---
threshold = 0.5  
df['no_context_binary'] = df['no_context_score'].apply(lambda x: 1 if x >= threshold else 0)
df['full_context_binary'] = df['full_context_score'].apply(lambda x: 1 if x >= threshold else 0)

# --- 2. Confusion Matrices ---

print("\n--- Confusion Matrix: No Context ---")
print(confusion_matrix(df['no_context_binary'], df['full_context_binary']))

print("\n--- Classification Report: No Context vs Full Context ---")
print(classification_report(df['no_context_binary'], df['full_context_binary'], target_names=['Non-Toxic', 'Toxic']))

# --- 3. Count predictions ---
print("\nPrediction Counts:")
print(df[['no_context_binary', 'full_context_binary']].value_counts())

# --- 4. Scatter plot: No-Context Score vs Full-Context Score ---

plt.figure(figsize=(8, 6))
plt.scatter(df['no_context_score'], df['full_context_score'], alpha=0.6)
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')  # Reference line y=x
plt.xlabel("Toxicity Score (No Context)", fontsize=12)
plt.ylabel("Toxicity Score (With Context)", fontsize=12)
plt.title("Perspective API: Effect of Context on Toxicity Scores", fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig("scatter_no_context_vs_full_context.png")
plt.show()

# --- Sort data into dictionary based on dialogue id ---


# --- Save with binary predictions added ---
df.to_csv("perspective_scores_dialoconan_binary.csv", index=False)

print("\nAnalysis complete. Files saved.")
