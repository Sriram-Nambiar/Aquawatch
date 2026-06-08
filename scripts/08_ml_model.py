import pandas as pd #reading, cleaning, and manipulating tabular data.
import os #file handling
import joblib #save and load ml models

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression #logistic regression, a statistical classification model.
from sklearn.preprocessing import StandardScaler #events features with large units (e.g., TDS) from dominating the model.
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

input_file = os.path.join("..", "output", "risk_table.csv")
model_file = os.path.join("..", "output", "logistic_risk_model.pkl")
df = pd.read_csv(input_file)

risk_map = {"Low": 0, "Medium": 1, "High": 2} # dictionary as enum type thing
df["Risk_encoded"] = df["Risk"].map(risk_map) #creates new column, mapping low to 0 so on...

features = ["pH", "BOD (mg/L)", "COD (mg/L)", "Total Dissolved Solids", "Total Coliform (MPN/100)"]
X = df[features]       #features
y = df["Risk_encoded"] #labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,  #75 training, 25 testing
    random_state=42, #ensure reproducible results.
    stratify=y   #same proportion of classes as the original full dataset
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        solver="lbfgs",
        max_iter=1000
    ))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(pipeline, model_file)
print(f"Model saved to {model_file}")
