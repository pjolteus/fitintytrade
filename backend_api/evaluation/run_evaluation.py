import argparse
from backtest_simulator import simulate_strategy
from performance_metrics import calculate_metrics
from export_to_pdf import export_report_to_pdf
from datetime import date, timedelta

def main(model, start, end, export):
    print(f"Running evaluation for model: {model} from {start} to {end}")
    results = simulate_strategy(start, end, model)
    metrics = calculate_metrics(results)

    if export:
        filepath = export_report_to_pdf(metrics, results)
        print(f"PDF report saved to {filepath}")
    else:
        print("Backtest Results:", results)
        print("Performance Metrics:", metrics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Model name (e.g., lstm_model)")
    parser.add_argument("--start", type=str, default=str(date.today() - timedelta(days=30)), help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=str(date.today()), help="End date (YYYY-MM-DD)")
    parser.add_argument("--export", action="store_true", help="Export to PDF")

    args = parser.parse_args()
    main(args.model, args.start, args.end, args.export)
