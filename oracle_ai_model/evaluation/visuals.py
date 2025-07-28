import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc

def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix", save_path=None):
    """
    Display a confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Purples", xticklabels=["Pred 0", "Pred 1"], yticklabels=["True 0", "True 1"])
    plt.title(title)
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_roc_curve(y_true, y_prob, title="ROC Curve", save_path=None):
    """
    Plot ROC curve with AUC.
    """
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, color="purple", lw=2, label=f"AUC = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend(loc="lower right")
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_prediction_vs_actual(y_true, y_prob, title="Prediction vs. Actual", save_path=None):
    """
    Line plot comparing prediction probabilities and true labels.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(y_prob, label="Predicted Probability", color="gold")
    plt.plot(y_true, label="True Label", color="purple", linestyle="--")
    plt.xlabel("Sample Index")
    plt.ylabel("Value")
    plt.title(title)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.show()
