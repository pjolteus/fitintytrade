# evaluation/thresholds_analysis.py
import torch
import numpy as np
from sklearn.metrics import roc_curve, f1_score
import plotly.graph_objs as go

def plot_roc_and_f1_threshold(model, dataloader, model_name="Model", device="cpu"):
    """
    Plot ROC curve and F1 score vs threshold curve using Plotly.
    """
    model.eval()
    probs, targets = [], []

    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            output = model(X_batch)
            prob = torch.sigmoid(output).squeeze()
            probs.extend(prob.cpu().numpy())
            targets.extend(y_batch.cpu().numpy())

    # Convert to NumPy arrays
    probs = np.array(probs)
    targets = np.array(targets)

    fpr, tpr, thresholds = roc_curve(targets, probs)
    f1_scores = [f1_score(targets, (probs > t).astype(int)) for t in thresholds]

    # Create Plotly traces
    trace_roc = go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve')
    trace_diag = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dot'))
    trace_f1 = go.Scatter(x=thresholds, y=f1_scores, mode='lines', name='F1 vs Threshold', yaxis='y2')

    # Layout with dual y-axes
    layout = go.Layout(
        title=f"{model_name} ROC & F1 Threshold Analysis",
        xaxis=dict(title='False Positive Rate'),
        yaxis=dict(title='True Positive Rate'),
        yaxis2=dict(title='F1 Score', overlaying='y', side='right', showgrid=False),
        legend=dict(x=0.7, y=0.2)
    )

    fig = go.Figure(data=[trace_roc, trace_diag, trace_f1], layout=layout)
    fig.show()

    return thresholds, f1_scores
