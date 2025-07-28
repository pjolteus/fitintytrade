# compare_models.py

import plotly.graph_objs as go
import numpy as np
import pandas as pd
import os

def compare_model_profit_curves(models_data, save_path=None, title="Model Profit Comparison"):
    """
    Plot and compare cumulative returns of different models.
    models_data: List of dicts with keys: 'name', 'df', where df contains ['cumulative_strategy']
    """
    fig = go.Figure()
    
    for model in models_data:
        name = model['name']
        df = model['df']
        if 'cumulative_strategy' not in df:
            continue
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['cumulative_strategy'],
            mode='lines',
            name=name
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Cumulative Return',
        template='plotly_white',
        legend=dict(x=0.01, y=0.99)
    )

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.write_html(save_path)
        print(f"[Compare] Saved plot to {save_path}")
    else:
        fig.show()


if __name__ == "__main__":
    # Example usage
    from evaluation.profit_curve import simulate_trades

    # Simulate 2 models
    prices = pd.Series(np.linspace(100, 110, 100) + np.random.randn(100))
    preds1 = np.random.rand(100)
    preds2 = np.random.rand(100)

    df1, *_ = simulate_trades(pd.DataFrame({'Close': prices}), preds1)
    df2, *_ = simulate_trades(pd.DataFrame({'Close': prices}), preds2)

    compare_model_profit_curves([
        {'name': 'LSTM', 'df': df1},
        {'name': 'Transformer', 'df': df2}
    ], save_path="outputs/profit_comparison.html")
