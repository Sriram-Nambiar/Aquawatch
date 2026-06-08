import pandas as pd
import os

# Path
input_file = os.path.join("..", "output", "cleaned_data.csv")
output_file = os.path.join("..", "output", "risk_table.csv")

# --- Load cleaned data CSV ---
df = pd.read_csv(input_file)

# Example limits based on Indian water standards set by CPCB
def classify_risk_with_reasons(row):
    violations = []

    if not (6.5 <= row['pH'] <= 8.5):
        violations.append("pH")
    if row['BOD (mg/L)'] > 3:
        violations.append("BOD (mg/L)")
    if row['COD (mg/L)'] > 10:
        violations.append("COD (mg/L)")
    if row['Total Dissolved Solids'] > 500:
        violations.append("Total Dissolved Solids")
    if row['Total Coliform (MPN/100)'] > 5000:
        violations.append("Total Coliform (MPN/100)")

    # # Risk begins after number of violations exceeds 2
    if len(violations) == 0:
        risk = "Low"
    elif len(violations) <= 2:
        risk = "Medium"
    else:
        risk = "High"

    return risk, ", ".join(violations)

# --- Apply classification, VVIMP STEP ---
df[['Risk', 'Risk_Reasons']] = df.apply(
    lambda row: pd.Series(classify_risk_with_reasons(row)),
    axis=1
)

risk_table = df[[
    "Name of Monitoring Station", "Year", "Sampling Month",
    "pH", "BOD (mg/L)", "COD (mg/L)", "Total Dissolved Solids", "Total Coliform (MPN/100)",
    "Latitude", "Longitude",
    "Risk", "Risk_Reasons"
]]
# --- Save risk table ---
risk_table.to_csv(output_file, index=False)
print(f"Risk table saved to {output_file}")
print(risk_table)
