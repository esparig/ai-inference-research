import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

# Generate dummy training data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])  # Simple y = 2x relationship

# Train a basic Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, "model.joblib")

print("Model trained and saved as model.joblib")
