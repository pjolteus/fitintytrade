from fastapi import APIRouter, Query
from evaluation.backtest_simulator import simulate_strategy
from evaluation.performance_metrics import calculate_metrics
from evaluation.export_to_pdf import export_report_to_pdf
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/evaluation/report")
def generate_evaluation_report(
    start_date: str = Query(...),
    end_date: str = Query(...),
    model_name: str = Query(...),
    export: bool = Query(default=False)
):
    backtest = simulate_strategy(start_date, end_date, model_name)
    metrics = calculate_metrics(backtest)

    if export:
        pdf_path = export_report_to_pdf(metrics, backtest)
        return FileResponse(pdf_path, media_type='application/pdf', filename='evaluation_report.pdf')
    
    return {
        "backtest": backtest,
        "metrics": metrics
    }
