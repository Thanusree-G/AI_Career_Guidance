import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
data = pd.read_csv("smart_career_dataset.csv")

# Input columns
X = data[["CurrentStage", "Stream", "Skill", "Interest", "Goal"]]

# Output columns (combine as one prediction)
y = data["RecommendedCourse"] + " | " + data["Career"] + " | " + data["FutureScope"]

# Encode input
encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model + encoders
joblib.dump(model, "career_model.pkl")
joblib.dump(encoders, "encoders.pkl")

print("AI Model trained successfully ✅")