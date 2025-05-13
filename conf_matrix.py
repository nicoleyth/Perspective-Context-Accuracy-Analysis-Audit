import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Loading data
df = pd.read_csv("perspective_score.csv")

# Binary Perspective API scores at threshold 0.5
df['predicted_label'] = (df['api_score'] >= 0.5).astype(int)

# Confusion matrix
cm = confusion_matrix(df['actual_score'], df['predicted_label'])

# Set up labels
labels = ['Non-Toxic', 'Toxic']

# Create the plot
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels)

plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.title('Perspective API: Confusion Matrix')
plt.tight_layout()

plt.savefig("perspective_conf_matrix.png", dpi=300)
plt.show()
