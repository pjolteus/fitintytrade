import pytest
from services.feature_extraction import get_features_for_ticker

def test_feature_extraction_valid():
    features = get_features_for_ticker(
        ticker="AAPL",
        interval="15m",
        window_size=30,
        selected_features=["rsi", "macd", "bbands"]
    )
    assert isinstance(features, list)
    assert all(isinstance(x, float) for x in features)
    assert len(features) > 0

def test_feature_extraction_invalid_ticker():
    features = get_features_for_ticker(
        ticker="INVALIDTICKER123",
        interval="15m",
        window_size=30,
        selected_features=["rsi", "macd"]
    )
    assert isinstance(features, list)
    assert all(x == 0.0 for x in features)

def test_feature_extraction_insufficient_data():
    features = get_features_for_ticker(
        ticker="AAPL",
        interval="1m",
        window_size=1000,  # intentionally too long
        selected_features=["rsi"]
    )
    assert isinstance(features, list)
    assert all(x == 0.0 for x in features)
