# indicators.py
import pandas as pd
import numpy as np

def add_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def add_macd(df, short=12, long=26, signal=9):
    ema_short = df['Close'].ewm(span=short, adjust=False).mean()
    ema_long = df['Close'].ewm(span=long, adjust=False).mean()
    df['macd'] = ema_short - ema_long
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    return df

def add_ema(df, span=20):
    df['ema'] = df['Close'].ewm(span=span, adjust=False).mean()
    return df

def add_atr(df, period=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = tr.rolling(window=period).mean()
    return df

def add_bollinger_bands(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    df['bb_upper'] = sma + (2 * std)
    df['bb_lower'] = sma - (2 * std)
    return df

def add_vwap(df):
    cum_volume_price = (df['Close'] * df['Volume']).cumsum()
    cum_volume = df['Volume'].cumsum()
    df['vwap'] = cum_volume_price / cum_volume
    return df

def add_adx(df, period=14):
    df['plus_dm'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']),
                             np.maximum(df['High'] - df['High'].shift(), 0), 0)
    df['minus_dm'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()),
                              np.maximum(df['Low'].shift() - df['Low'], 0), 0)
    tr = pd.concat([
        df['High'] - df['Low'],
        np.abs(df['High'] - df['Close'].shift()),
        np.abs(df['Low'] - df['Close'].shift())
    ], axis=1).max(axis=1)
    tr_smooth = tr.rolling(window=period).mean()
    plus_di = 100 * (df['plus_dm'].rolling(window=period).mean() / tr_smooth)
    minus_di = 100 * (df['minus_dm'].rolling(window=period).mean() / tr_smooth)
    df['adx'] = (np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)) * 100
    return df

