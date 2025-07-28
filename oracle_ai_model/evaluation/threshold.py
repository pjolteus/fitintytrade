import numpy as np
from sklearn.metrics import f1_score

def tune_threshold(y_true, y_prob, metric="f1", step=0.01):
    best_threshold = 0.5
    best_score = -1
    thresholds = np.arange(0.0, 1.0, step)

    for threshold in thresholds:
        y_pred = (y_prob > threshold).astype(int)
        if metric == "f1":
            score = f1_score(y_true, y_pred)
        # Optionally add: precision, recall, profit here

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold, best_score
