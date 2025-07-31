# indicators.py
import pandas as pd
import numpy as np

def add_rsi(df: pd.DataFrame, period: int = 14, inplace: bool = True) -> pd.DataFrame:
    delta = df['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    if inplace:
        df['rsi'] = rsi
        return df
    return rsi.to_frame(name="rsi")

def add_macd(df: pd.DataFrame, short: int = 12, long: int = 26, signal: int = 9, inplace: bool = True) -> pd.DataFrame:
    ema_short = df['Close'].ewm(span=short, adjust=False).mean()
    ema_long = df['Close'].ewm(span=long, adjust=False).mean()
    macd = ema_short - ema_long
    macd_signal = macd.ewm(span=signal, adjust=False).mean()

    if inplace:
        df['macd'] = macd
        df['macd_signal'] = macd_signal
        return df
    return pd.concat([macd.rename("macd"), macd_signal.rename("macd_signal")], axis=1)

def add_ema(df: pd.DataFrame, span: int = 20, inplace: bool = True) -> pd.DataFrame:
    ema = df['Close'].ewm(span=span, adjust=False).mean()
    if inplace:
        df[f'ema_{span}'] = ema
        return df
    return ema.to_frame(name=f"ema_{span}")

def add_atr(df: pd.DataFrame, period: int = 14, inplace: bool = True) -> pd.DataFrame:
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    if inplace:
        df['atr'] = atr
        return df
    return atr.to_frame(name="atr")

def add_bollinger_bands(df: pd.DataFrame, period: int = 20, inplace: bool = True) -> pd.DataFrame:
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)

    if inplace:
        df['bb_upper'] = upper
        df['bb_lower'] = lower
        return df
    return pd.concat([upper.rename("bb_upper"), lower.rename("bb_lower")], axis=1)

def add_vwap(df: pd.DataFrame, inplace: bool = True) -> pd.DataFrame:
    cum_volume_price = (df['Close'] * df['Volume']).cumsum()
    cum_volume = df['Volume'].cumsum()
    vwap = cum_volume_price / (cum_volume + 1e-10)

    if inplace:
        df['vwap'] = vwap
        return df
    return vwap.to_frame(name="vwap")

def add_adx(df: pd.DataFrame, period: int = 14, inplace: bool = True) -> pd.DataFrame:
    plus_dm = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']),
                       np.maximum(df['High'] - df['High'].shift(), 0), 0)
    minus_dm = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()),
                        np.maximum(df['Low'].shift() - df['Low'], 0), 0)
    
    tr = pd.concat([
        df['High'] - df['Low'],
        np.abs(df['High'] - df['Close'].shift()),
        np.abs(df['Low'] - df['Close'].shift())
    ], axis=1).max(axis=1)
    tr_smooth = tr.rolling(window=period).mean()

    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / (tr_smooth + 1e-10))
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / (tr_smooth + 1e-10))
    adx = (np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)) * 100

    if inplace:
        df['adx'] = adx
        return df
    return adx.to_frame(name="adx")

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds all technical indicators to the DataFrame in-place.
    """
    add_rsi(df)
    add_macd(df)
    add_ema(df)
    add_atr(df)
    add_bollinger_bands(df)
    add_vwap(df)
    add_adx(df)
    return df
