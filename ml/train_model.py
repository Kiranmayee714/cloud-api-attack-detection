import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# load feature dataset
df = pd.read_csv("data/api_features.csv")

# remove IP column (not useful for ML)
X = df.drop("ip", axis=1)

# create model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# train model
model.fit(X)

# save model
joblib.dump(model, "model/api_attack_model.pkl")

print("Model trained successfully!")

# test predictions
predictions = model.predict(X)

df["anomaly"] = predictions

print("\nPrediction sample:")
print(df.head())

import numpy as np

anomaly_count = np.sum(predictions == -1)
normal_count = np.sum(predictions == 1)

print("\nModel Evaluation:")
print("Normal behaviour detected:", normal_count)
print("Suspicious behaviour detected:", anomaly_count)