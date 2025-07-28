from .indicators import (
    add_rsi,
    add_macd,
    add_ema,
    add_atr,
    add_bollinger_bands,
    add_adx,
    add_vwap
)

def add_technical_indicators(df):
    df = add_rsi(df)
    df = add_macd(df)
    df = add_ema(df)
    df = add_atr(df)
    df = add_bollinger_bands(df)
    df = add_adx(df)
    df = add_vwap(df)
    return df

def normalize(df, columns, method="zscore"):
    """
    Normalize the selected columns of the DataFrame using the specified method.
    Options: 'zscore', 'minmax'
    """
    if method == "zscore":
        for col in columns:
            df[col] = (df[col] - df[col].mean()) / df[col].std()
    elif method == "minmax":
        for col in columns:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    else:
        raise ValueError("Unsupported normalization method. Use 'zscore' or 'minmax'.")
    return df

def export_features_csv(df, filename="features_snapshot.csv"):
    """
    Export DataFrame to CSV for debugging/visualization.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"[INFO] Features exported to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to export features: {e}")

