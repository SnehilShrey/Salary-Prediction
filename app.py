import streamlit as st
import numpy as np
import pandas as pd
import joblib
import base64

# Load model and features
model = joblib.load('salary_model.pkl')
model_features = joblib.load('model_features.pkl')

def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image
set_background("background.jpg")

st.title("💼 Salary Prediction System")
st.write("Enter the details below to predict whether the annual income is more than $50K or not.")

# ℹ️ Information about currency
st.info("💡 All monetary values (Capital Gain, Capital Loss, etc.) are in **U.S. Dollars (USD)** as per U.S. Census dataset.")

# Input fields
age = st.slider("Age", 18, 90, 30)
education_num = st.slider("Education Level (numeric)", 1, 16, 10)
hours_per_week = st.slider("Hours Worked per Week", 1, 100, 40)
capital_gain = st.number_input("Capital Gain (USD)", min_value=0, max_value=99999, value=0)
capital_loss = st.number_input("Capital Loss (USD)", min_value=0, max_value=4356, value=0)

# Select boxes for categorical values
gender = st.selectbox("Gender", ["Male", "Female"])
relationship = st.selectbox("Relationship", ["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other"])
race = st.selectbox("Race", ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"])
marital_status = st.selectbox("Marital Status", ["Never-married", "Married-civ-spouse", "Divorced", "Separated", "Widowed", "Married-spouse-absent"])

# Prepare input dictionary with default values
input_dict = {
    'age': age,
    'educational-num': education_num,
    'hours-per-week': hours_per_week,
    'capital-gain': capital_gain,
    'capital-loss': capital_loss,
}

# Set all one-hot encoded columns to 0
for col in model_features:
    if col not in input_dict:
        input_dict[col] = 0

# Set appropriate one-hot encoded values based on user input
input_dict[f'gender_{gender}'] = 1
input_dict[f'relationship_{relationship}'] = 1
input_dict[f'race_{race}'] = 1
input_dict[f'marital-status_{marital_status}'] = 1

# Create input DataFrame
input_df = pd.DataFrame([input_dict])[model_features]

# Predict on button click
if st.button("Predict Salary Class"):
    prediction = model.predict(input_df)[0]
    income_class = ">50K" if prediction == 1 else "<=50K"
    st.success(f"✅ Predicted Income: **{income_class}**")