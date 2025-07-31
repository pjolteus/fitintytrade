
import pandas as pd
import numpy as np

def compute_performance_metrics(df, capital=10000):
    df = df.copy()
    df['profit_pct'] = df['profit'] / capital
    df['cumulative_return'] = (1 + df['profit_pct']).cumprod()

    total_return = df['cumulative_return'].iloc[-1] - 1
    daily_returns = df['profit_pct']
    annualized_return = (1 + total_return) ** (252 / len(df)) - 1
    volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (annualized_return - 0.02) / volatility if volatility else 0

    cumulative = df['cumulative_return']
    max_drawdown = ((cumulative.cummax() - cumulative) / cumulative.cummax()).max()

    return {
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown
    }
