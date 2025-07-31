import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FitintyTrade Admin", layout="wide")
st.title("📊 FitintyTrade Admin Panel")

token = st.text_input("Enter Admin JWT Token", type="password")

if token:
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch data
    alerts = requests.get("http://localhost:8000/admin/alerts", headers=headers).json()
    predictions = requests.get("http://localhost:8000/admin/predictions", headers=headers).json()

    # Convert to DataFrames
    df_alerts = pd.DataFrame(alerts)
    df_preds = pd.DataFrame(predictions)

    # ---------------- Alerts Section ----------------
    st.subheader("🔔 Alert Logs")

    if not df_alerts.empty:
        col1, col2 = st.columns(2)

        with col1:
            selected_type = st.selectbox("Filter by Alert Type", options=["All"] + df_alerts["type"].unique().tolist())
        with col2:
            search_symbol = st.text_input("Search Symbol")

        filtered_alerts = df_alerts.copy()
        if selected_type != "All":
            filtered_alerts = filtered_alerts[filtered_alerts["type"] == selected_type]
        if search_symbol:
            filtered_alerts = filtered_alerts[filtered_alerts["symbol"].str.contains(search_symbol.upper())]

        st.dataframe(filtered_alerts)

        csv = filtered_alerts.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export Alerts CSV", csv, "alerts.csv", "text/csv")

    # ---------------- Predictions Section ----------------
    st.subheader("📈 Prediction Results")

    if not df_preds.empty:
        col3, col4 = st.columns(2)

        with col3:
            selected_feedback = st.selectbox("Filter by Feedback", options=["All"] + df_preds["feedback"].dropna().unique().tolist())
        with col4:
            search_ticker = st.text_input("Search Ticker")

        filtered_preds = df_preds.copy()
        if selected_feedback != "All":
            filtered_preds = filtered_preds[filtered_preds["feedback"] == selected_feedback]
        if search_ticker:
            filtered_preds = filtered_preds[filtered_preds["ticker"].str.contains(search_ticker.upper())]

        st.dataframe(filtered_preds)

        csv2 = filtered_preds.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export Predictions CSV", csv2, "predictions.csv", "text/csv")

<Button onClick={handleDownloadPDF}>Download Evaluation PDF</Button>

const handleDownloadPDF = async () => {
  const res = await fetch('/api/evaluation/report?start_date=2024-07-01&end_date=2024-07-27&model_name=lstm_model&export=true');
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'evaluation_report.pdf';
  a.click();
};
