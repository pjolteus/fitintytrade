
import pandas as pd

def rolling_backtest(df, capital=10000, lookback_days=30, top_n=5):
    df = df.sort_values(by='date')
    daily_capital = capital / (len(df['date'].unique()) or 1)
    history = []

    for date in df['date'].unique():
        day_df = df[df['date'] == date]
        selected = day_df.sort_values(by='confidence', ascending=False).head(top_n)
        profit = selected['profit'].sum()
        history.append({
            "date": date,
            "daily_profit": profit,
            "capital": daily_capital,
            "return": profit / daily_capital
        })

    return pd.DataFrame(history)
