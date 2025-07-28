# evaluation/comparison.py

import os
import json
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def compare_profit_curves(metrics_list, model_names, save_path=None):
    """
    Plot cumulative strategy returns for multiple models.
    Each metrics entry must include 'cumulative_strategy'.
    """
    plt.figure(figsize=(10, 5))
    for metrics, name in zip(metrics_list, model_names):
        if "Cumulative Strategy" in metrics:
            plt.plot(metrics["Cumulative Strategy"], label=f"{name}")
    plt.title("Profit Curve Comparison")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()


def compare_roc_curves(metrics_list, model_names, save_path=None):
    """
    Plot ROC curves for multiple models using true labels and probabilities.
    """
    plt.figure(figsize=(7, 5))
    for metrics, name in zip(metrics_list, model_names):
        if "Targets" in metrics and "Probabilities" in metrics:
            fpr, tpr, _ = roc_curve(metrics["Targets"], metrics["Probabilities"])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f"{name} (AUC={roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.title("ROC Curve Comparison")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    if save_path:
        plt.savefig(save_path)
    plt.show()


def load_metrics_files(json_paths):
    """
    Load multiple saved evaluation JSON metrics.
    """
    metrics_list = []
    for path in json_paths:
        with open(path, "r") as f:
            metrics = json.load(f)
        metrics_list.append(metrics)
    return metrics_list
