import pandas as pd
import matplotlib.pyplot as plt
import os

# Path
input_file = os.path.join("..", "output", "risk_table.csv")
output_dir = os.path.join("..", "output")
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(input_file)


df['Date'] = pd.to_datetime(df['Year'].astype(str) + "-" + df['Sampling Month'].astype(str) + "-01") # time column
df = df.sort_values('Date') # Sort by time

# -----------------------------
# Monthly risk counts table
# -----------------------------
monthly_risk = (
    df.groupby([df['Date'].dt.to_period('M'), 'Risk'])
      .size()
      .unstack(fill_value=0)
)
monthly_risk = monthly_risk.sort_index()

# -----------------------------
# Plot stacked bar chart
# -----------------------------
monthly_risk.plot(
    kind='bar',
    stacked=True,
    figsize=(12,6),
    color={'Low':'green', 'Medium':'orange', 'High':'red'}
)

plt.title("Monthly Lake Risk Distribution")
plt.xlabel("Sampling Month")
plt.ylabel("Number of Lakes")
plt.xticks(rotation=45)
plt.tight_layout()

out_file = os.path.join(output_dir, "monthly_risk_distribution.png")
plt.savefig(out_file)
plt.close()

print(f"Saved: {out_file}")

# -----------------------------
# High-risk trend plot
# -----------------------------
high_risk_trend = (
    df[df['Risk'] == 'High']
    .groupby(df['Date'].dt.to_period('M'))
    .size()
)

high_risk_trend.plot(
    kind='line',
    marker='o',
    figsize=(10,5),
    color='red'
)

plt.title("Trend of High-Risk Lakes Over Time")
plt.xlabel("Sampling Month")
plt.ylabel("Number of High-Risk Lakes")
plt.grid(True)
plt.tight_layout()

out_file = os.path.join(output_dir, "high_risk_trend.png")
plt.savefig(out_file)
plt.close()

print(f"Saved: {out_file}")
