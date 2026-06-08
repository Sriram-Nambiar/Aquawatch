import pandas as pd
import os

# Path
data_file = os.path.join("..", "data", "master_water_data.csv")
output_file = os.path.join("..", "output", "cleaned_data.csv")

# --- Load CSV ---
df = pd.read_csv(data_file)  # reading with pandas
print("Original data:")
print(df.head())  # .head() returns the first n rows

# --- Keep only relevant columns (drop extra if any)---
columns_needed = ["Name of Monitoring Station", "Year", "Sampling Month", "pH", "BOD (mg/L)", "COD (mg/L)", "Total Dissolved Solids", "Total Coliform (MPN/100)", "Latitude", "Longitude"]
df = df[columns_needed]  # header of csv

# Drop rows with more than 2 missing values,
df = df[df.isnull().sum(axis=1) <= 2]

# Fill remaining missing values with column mean using pandas
df.fillna(df.mean(numeric_only=True), inplace=True)

# -----Save-----
os.makedirs(os.path.join("..","output"), exist_ok=True)
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to {output_file}")
