# evaluation/compare_models_plotly.py
import plotly.graph_objs as go
import torch
import numpy as np
from evaluation.profit_curve import simulate_trades


def compare_models_profit(models_info, df_prices, threshold=0.5):
    """
    Compare multiple models on profit curve with Plotly.
    models_info: list of dicts with keys:
        - name: str
        - model: PyTorch model
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

        df_result, profit, _ = simulate_trades(df_prices.copy(), np.array(probs), threshold=threshold)

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
