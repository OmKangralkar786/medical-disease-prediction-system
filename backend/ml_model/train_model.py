import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("dataset.csv")

# Remove Unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Clean column names
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_", regex=False)
)

# Fix duplicate column names
new_columns = []
seen = set()

for col in df.columns:
    if col.endswith(".1"):
        continue
    if col not in seen:
        new_columns.append(col)
        seen.add(col)

df = df[new_columns]

X = df.drop("disease", axis=1)
y = df["disease"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "disease_model.pkl")
joblib.dump(list(X.columns), "symptoms.pkl")

print("Training Complete")