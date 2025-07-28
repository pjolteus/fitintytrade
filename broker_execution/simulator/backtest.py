
def backtest_strategy(price_data, strategy_fn):
    results = []
    for i in range(len(price_data)):
        signal = strategy_fn(price_data[:i+1])
        results.append(signal)
    return results
