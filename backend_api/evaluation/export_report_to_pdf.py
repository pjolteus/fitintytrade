import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import tempfile
from fpdf import FPDF
from datetime import datetime
import os

def export_report_to_pdf(metrics: dict, backtest: list, filename=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "FitintyTrade Evaluation Report", ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Performance Metrics", ln=True)

    pdf.set_font("Arial", "", 12)
    for key, value in metrics.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    # Plot and insert profit curve
    profit_img = plot_profit_curve(backtest)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Profit Curve", ln=True)
    pdf.image(profit_img, x=10, y=30, w=190)

    # Optional: Plot and insert confusion matrix
    if all("actual" in t and "predicted" in t for t in backtest):
        cm_img = plot_conf_matrix(
            [t["actual"] for t in backtest],
            [t["predicted"] for t in backtest]
        )
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Confusion Matrix", ln=True)
        pdf.image(cm_img, x=10, y=30, w=190)

    # Add sample trades
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Sample Backtest Trades", ln=True)
    pdf.set_font("Arial", "", 11)
    for trade in backtest[:10]:
        pdf.multi_cell(0, 10, str(trade))

    # Output
    if not filename:
        filename = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("backend_api/evaluation/reports", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pdf.output(filepath)

    # Clean temp images
    try:
        os.remove(profit_img)
        if 'cm_img' in locals():
            os.remove(cm_img)
    except Exception as e:
        print("Cleanup failed:", e)

    return filepath

def plot_profit_curve(results):
    cumulative = [0]
    for trade in results:
        cumulative.append(cumulative[-1] + trade.get('profit', 0))

    plt.figure(figsize=(6, 3))
    plt.plot(cumulative, label="Profit Curve", linewidth=2, color='green')
    plt.title("Cumulative Profit Over Time")
    plt.xlabel("Trades")
    plt.ylabel("Profit ($)")
    plt.grid(True)
    plt.tight_layout()

    img_path = tempfile.mktemp(suffix=".png")
    plt.savefig(img_path)
    plt.close()
    return img_path

def plot_conf_matrix(true_labels, predictions):
    cm = confusion_matrix(true_labels, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues", values_format="d")

    img_path = tempfile.mktemp(suffix=".png")
    plt.savefig(img_path)
    plt.close()
    return img_path
