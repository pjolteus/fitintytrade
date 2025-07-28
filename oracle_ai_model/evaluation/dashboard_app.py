//dashboard_app.py
import plotly.graph_objs as go
from evaluation.profit_curve import simulate_trades
from sklearn.metrics import roc_curve, auc, f1_score
import numpy as np
import pandas as pd
import torch


def compare_models_profit(models_info, df_prices, threshold=0.5):
    """
    Compare multiple models on profit curve.
    models_info: list of dicts with keys:
        - name: str
        - model: PyTorch model object
        - dataloader: PyTorch DataLoader
    """
    traces = []

    for info in models_info:
        name = info['name']
        model = info['model']
        dataloader = info['dataloader']

        model.eval()
        probs = []

        with torch.no_grad():
            for X_batch, _ in dataloader:
                X_batch = X_batch.to(next(model.parameters()).device)
                output = model(X_batch)
                prob = torch.sigmoid(output).squeeze()
                probs.extend(prob.cpu().numpy())

        df_result, profit, benchmark = simulate_trades(df_prices.copy(), np.array(probs), threshold=threshold)

        traces.append(go.Scatter(
            x=df_result.index,
            y=df_result['cumulative_strategy'],
            mode='lines',
            name=f"{name} (Profit=${profit:.2f})"
        ))

    # Market benchmark
    df_prices['returns'] = df_prices['Close'].pct_change().fillna(0)
    df_prices['cumulative_returns'] = (1 + df_prices['returns']).cumprod()
    traces.append(go.Scatter(
        x=df_prices.index,
        y=df_prices['cumulative_returns'],
        mode='lines',
        name="Market Benchmark",
        line=dict(dash='dot')
    ))

    layout = go.Layout(
        title="Model Profit Comparison",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Cumulative Return"),
        hovermode='closest'
    )
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


def plot_roc_threshold(model, dataloader, model_name="Model", device="cpu"):
    model.eval()
    probs, targets = [], []

    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            output = model(X_batch)
            prob = torch.sigmoid(output).squeeze()
            probs.extend(prob.cpu().numpy())
            targets.extend(y_batch.cpu().numpy())

    fpr, tpr, thresholds = roc_curve(targets, probs)
    f1_scores = [f1_score(targets, (np.array(probs) > t).astype(int)) for t in thresholds]

    trace_roc = go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve')
    trace_diag = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dot'))
    trace_f1 = go.Scatter(x=thresholds, y=f1_scores, mode='lines', name='F1 vs Threshold', yaxis='y2')

    layout = go.Layout(
        title=f"{model_name} ROC & F1 Threshold Analysis",
        xaxis=dict(title='False Positive Rate'),
        yaxis=dict(title='True Positive Rate'),
        yaxis2=dict(title='F1 Score', overlaying='y', side='right', showgrid=False),
        legend=dict(x=0.7, y=0.2)
    )

    fig = go.Figure(data=[trace_roc, trace_diag, trace_f1], layout=layout)
    fig.show()
