# evaluation/profit_curve.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simulate_trades(df, preds, threshold=0.5, trade_amount=1000):
    """
    Simulates profit/loss from prediction signals.
    - Buys (long) when prediction > threshold
    - Sells (short) when prediction < (1 - threshold)
    """
    df = df.copy()
    df['signal'] = 0
    df.loc[preds > threshold, 'signal'] = 1
    df.loc[preds < (1 - threshold), 'signal'] = -1

    df['returns'] = df['Close'].pct_change().fillna(0)
    df['strategy'] = df['signal'].shift(1) * df['returns']
    df['strategy'].fillna(0, inplace=True)
    df['cumulative_returns'] = (1 + df['returns']).cumprod()
    df['cumulative_strategy'] = (1 + df['strategy']).cumprod()

    profit = (df['cumulative_strategy'].iloc[-1] - 1) * trade_amount
    benchmark = (df['cumulative_returns'].iloc[-1] - 1) * trade_amount

    return df, profit, benchmark


def plot_profit_curve(df, save_path=None):
    plt.figure(figsize=(10, 5))
    plt.plot(df['cumulative_returns'], label='Market Return')
    plt.plot(df['cumulative_strategy'], label='Strategy Return', linestyle='--')
    plt.title('Profit Curve')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()


if __name__ == "__main__":
    # Demo with dummy data
    data = pd.read_csv("../oracle_ai_model/data/sample.csv")  # Example CSV with Close prices
    dummy_preds = np.random.rand(len(data))
    result_df, profit, benchmark = simulate_trades(data, dummy_preds)
    print(f"Profit: ${profit:.2f}, Benchmark: ${benchmark:.2f}")
    plot_profit_curve(result_df)

