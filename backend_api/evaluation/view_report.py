import streamlit as st
import json
import os
from evaluation.export_report_to_pdf import (
    export_report_to_pdf,
    plot_profit_curve,
    plot_conf_matrix,
)
from evaluation.performance_metrics import calculate_metrics

st.set_page_config(page_title="FitintyTrade Report Viewer", layout="wide")

st.title("📈 FitintyTrade Evaluation Report Viewer")
st.markdown("Upload your backtest results (JSON) or view a demo report.")

# === File uploader or use sample
uploaded_file = st.file_uploader("Upload Backtest JSON", type=["json"])

if uploaded_file:
    data = json.load(uploaded_file)
    backtest = data if isinstance(data, list) else data.get("results", [])
else:
    st.markdown("---")
    st.subheader("🚀 Demo Sample")
    from evaluation.backtest_simulator import simulate_strategy
    backtest = simulate_strategy("2024-07-01", "2024-07-27")

if not backtest:
    st.warning("No backtest results found.")
    st.stop()

# === Metrics
metrics = calculate_metrics(backtest)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔍 Performance Metrics")
    for key, value in metrics.items():
        st.write(f"**{key}**: {value}")

# === Profit Curve
st.subheader("📊 Profit Curve")
profit_img = plot_profit_curve(backtest)
st.image(profit_img, use_column_width=True)

# === Confusion Matrix (optional)
if all("actual" in t and "predicted" in t for t in backtest):
    st.subheader("📘 Confusion Matrix")
    cm_img = plot_conf_matrix(
        [t["actual"] for t in backtest],
        [t["predicted"] for t in backtest]
    )
    st.image(cm_img, use_column_width=True)

# === Export Button
st.subheader("📥 Export Report to PDF")
if st.button("📄 Generate PDF Report"):
    path = export_report_to_pdf(metrics, backtest)
    with open(path, "rb") as f:
        st.download_button("⬇️ Download Report", data=f, file_name=os.path.basename(path))
