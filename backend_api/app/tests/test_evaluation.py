from evaluation.backtest_simulator import simulate_strategy
from evaluation.performance_metrics import calculate_metrics
from evaluation.export_report_to_pdf import export_report_to_pdf

def test_simulate_strategy():
    results = simulate_strategy("2024-07-01", "2024-07-27", "lstm_model")
    assert isinstance(results, list)
    assert all("profit" in r for r in results)

def test_performance_metrics():
    results = simulate_strategy("2024-07-01", "2024-07-27", "lstm_model")
    metrics = calculate_metrics(results)
    assert "Total Trades" in metrics
    assert "Profit Factor" in metrics

def test_pdf_export():
    results = simulate_strategy("2024-07-01", "2024-07-27", "lstm_model")
    metrics = calculate_metrics(results)
    filepath = export_report_to_pdf(metrics, results)
    assert filepath.endswith(".pdf")
