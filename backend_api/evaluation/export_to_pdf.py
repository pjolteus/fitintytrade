
from fpdf import FPDF

def export_metrics_to_pdf(metrics: dict, filename="performance_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="FitintyTrade Performance Summary", ln=True)

    for k, v in metrics.items():
        pdf.cell(200, 10, txt=f"{k}: {v:.4f}", ln=True)

    pdf.output(filename)
