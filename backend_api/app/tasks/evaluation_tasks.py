from celery_app.worker import celery
from evaluation.backtest_simulator import simulate_strategy
from evaluation.performance_metrics import calculate_metrics
from evaluation.export_to_pdf import export_report_to_pdf
import datetime

@celery.task
def daily_model_evaluation():
    today = datetime.date.today()
    start = str(today - datetime.timedelta(days=30))
    end = str(today)
    model = "lstm_model"

    backtest = simulate_strategy(start, end, model)
    metrics = calculate_metrics(backtest)
    export_report_to_pdf(metrics, backtest)

@celery.task(name="run_scheduled_evaluation")
def run_scheduled_evaluation(model: str, start: str, end: str):
    results = simulate_strategy(start, end, model)
    metrics = calculate_metrics(results)
    path = export_report_to_pdf(metrics, results)
    return {"status": "complete", "report_path": path}