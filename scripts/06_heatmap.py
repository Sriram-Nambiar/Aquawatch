import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import joblib

# Path
risk_file = os.path.join("..", "output", "risk_table.csv")
cleaned_file = os.path.join("..", "output", "cleaned_data.csv")
model_file = os.path.join("..", "output", "logistic_risk_model.pkl")

current_map_file = os.path.join("..", "output", "heatmap_current.html")
predicted_map_file = os.path.join("..", "output", "heatmap_predicted.html")

# Load data
risk_df = pd.read_csv(risk_file)
clean_df = pd.read_csv(cleaned_file)

model = joblib.load(model_file)

# -----Intensity mapping----

risk_intensity = {"Low": 1, "Medium": 5, "High": 10}
color_map = {"Low": "green", "Medium": "orange", "High": "purple"}

# Low is redundant as there exist no Low risk lakes present within dataset
def create_heatmap(df, risk_col, output_file, title):
    df["Intensity"] = df[risk_col].map(risk_intensity)

    m = folium.Map(location=[12.9716, 77.5946], zoom_start=11)  # approx bounds of bangalore

    heat_data = [
        [row["Latitude"], row["Longitude"], row["Intensity"]]
        for _, row in df.iterrows()
    ]

    HeatMap(
        heat_data,
        min_opacity=0.2,
        radius=62.5,
        blur=30,
        max_zoom=11
    ).add_to(m)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=6,
            color=color_map[row[risk_col]],
            fill=True,
            fill_color=color_map[row[risk_col]],
            fill_opacity=0.8,
            tooltip=f"{row['Name of Monitoring Station']}<br>{title} Risk: {row[risk_col]}"
        ).add_to(m)

    m.save(output_file)
    print(f"Saved {title} heatmap → {output_file}")

# ----------------------------
# 1️⃣ CURRENT (Rule-based)
# ----------------------------
create_heatmap(
    risk_df,
    risk_col="Risk",
    output_file=current_map_file,
    title="Current"
)

# ----------------------------
# 2️⃣ PREDICTED (ML-based)
# ----------------------------
features = ["pH", "BOD (mg/L)", "COD (mg/L)", "Total Dissolved Solids", "Total Coliform (MPN/100)"]
preds = model.predict(clean_df[features])

inv_map = {0: "Low", 1: "Medium", 2: "High"}
clean_df["Predicted_Risk"] = preds
clean_df["Predicted_Risk"] = clean_df["Predicted_Risk"].map(inv_map)

pred_df = clean_df[["Name of Monitoring Station", "Latitude", "Longitude", "Predicted_Risk"]]

create_heatmap(
    pred_df,
    risk_col="Predicted_Risk",
    output_file=predicted_map_file,
    title="Predicted"
)
