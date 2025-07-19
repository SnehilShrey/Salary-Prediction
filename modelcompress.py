import joblib

# Load your original big model
model = joblib.load('salary_model.pkl')

# Save a compressed version (maximum compression level 9)
joblib.dump(model, 'salary_model_compressed.pkl', compress=9)

print("Model compressed and saved as 'salary_model_compressed.pkl'")