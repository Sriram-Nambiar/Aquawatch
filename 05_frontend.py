import streamlit as st
import pandas as pd
import joblib
from streamlit.components.v1 import html

# --------------------------
# Page configuration via streamlit
# --------------------------
st.set_page_config(page_title="Lake Risk Dashboard", layout="wide")
st.title("Urban Lake Risk Monitoring Dashboard")

mode = st.sidebar.radio(
    "Select View",
    ["Current Risk (Rule-based)", "Predicted Risk (ML Model)"]
)

# --------------------------
# Map display (HTML EMBED OF PREVIOUSLY MADE HEATMAPS IN 06_heatmap.py)
# --------------------------
st.subheader("Lake Risk Heatmap")

if mode == "Current Risk (Rule-based)":
    with open("output/heatmap_current.html", "r", encoding="utf-8") as f:
        html(f.read(), height=550)

else:
    with open("output/heatmap_predicted.html", "r", encoding="utf-8") as f:
        html(f.read(), height=550)

# --------------------------
# Data table
# --------------------------
st.subheader("Lake Risk Table")

if mode == "Current Risk (Rule-based)":
    df = pd.read_csv("output/risk_table.csv")
    st.dataframe(
        df[["Name of Monitoring Station", "Year", "Sampling Month", "Risk"]],
        use_container_width=True
    )
else:
    df = pd.read_csv("output/cleaned_data.csv")
    model = joblib.load("output/logistic_risk_model.pkl")

    features = ["pH", "BOD (mg/L)", "COD (mg/L)", "Total Dissolved Solids", "Total Coliform (MPN/100)"]
    preds = model.predict(df[features])

    inv_map = {0: "Low", 1: "Medium", 2: "High"}
    df["Predicted_Risk"] = preds
    df["Predicted_Risk"] = df["Predicted_Risk"].map(inv_map)

    st.dataframe(
        df[["Name of Monitoring Station", "Year", "Sampling Month", "Predicted_Risk"]],
        use_container_width=True
    )

# --------------------------
# Disclaimer paragraph
# --------------------------
st.caption(
    "⚠️ This dashboard is a decision-support and visualization tool. "
    "It is based on historical government water quality data and does not "
    "represent real-time water safety certification."
)
