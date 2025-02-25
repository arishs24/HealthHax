import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Generate synthetic dataset
np.random.seed(42)
num_samples = 1000
data = {
    "Age": np.random.randint(30, 85, num_samples),
    "Sex": np.random.choice([0, 1], num_samples),
    "Chest_Pain": np.random.choice([0, 1, 2], num_samples),
    "Dizziness": np.random.choice([0, 1], num_samples),
    "Shoulder_Pain": np.random.choice([0, 1], num_samples),
    "Fatigue": np.random.choice([0, 1], num_samples),
    "ECG_Abnormality": np.random.choice([0, 1], num_samples),
    "Troponin_Level": np.random.uniform(0.01, 0.1, num_samples),
    "Hypertension": np.random.choice([0, 1], num_samples),
    "Diabetes": np.random.choice([0, 1], num_samples),
    "Prior_Heart_Disease": np.random.choice([0, 1], num_samples),
    "MI_Diagnosis": np.random.choice([0, 1], num_samples, p=[0.85, 0.15])
}

df = pd.DataFrame(data)
X = df.drop(columns=["MI_Diagnosis"])
y = df["MI_Diagnosis"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
model.fit(X_train_scaled, y_train)

# Save model & scaler
with open("mi_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model & Scaler saved successfully!")
