import subprocess
import streamlit as st
import pandas as pd
from performance_metrics import compute_performance_metrics
from backtest_simulator import rolling_backtest
from analytics.by_asset_type import performance_by_asset_class

st.title("📊 FitintyTrade Strategy Dashboard")

uploaded = st.file_uploader("Upload Prediction Result CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.write("Sample Data", df.head())

    metrics = compute_performance_metrics(df)
    st.subheader("Performance Metrics")
    st.json(metrics)

    st.subheader("Backtest Simulation")
    sim_df = rolling_backtest(df)
    st.line_chart(sim_df.set_index("date")["daily_profit"])

    st.subheader("Asset Breakdown")
    st.dataframe(performance_by_asset_class(df))

#dashboard_launcher.py
def launch_dashboard():
    subprocess.run(["streamlit", "run", "backend_api/evaluation/dashboard_app.py"])
