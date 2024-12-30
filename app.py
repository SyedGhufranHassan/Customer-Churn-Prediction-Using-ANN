## Import Libraries
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf 
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle
from tensorflow.keras.models import load_model


#Load all the trained model, scaler, label_encoding, one_hot_encoding
model=load_model('ANN_model.h5')


#Load the scaler and encdoer
with open('encoder_gender.pkl','rb') as file:
    encoder_gender=pickle.load(file)
    
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)
    
with open('one_hot_encoding_geography.pkl','rb') as file:
    one_hot_encoding_geography=pickle.load(file)
    
## Stream lit app
st.title('Customer Churn Prediction')

# User input
geography = st.selectbox('Geography', one_hot_encoding_geography.categories_[0])
gender = st.selectbox('Gender', encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# One-hot encode 'Geography'
geo_encoded = one_hot_encoding_geography.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=one_hot_encoding_geography.get_feature_names_out(['Geography']))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale the input data
input_data_scaled = scaler.transform(input_data)


# Predict churn
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write(f'Churn Probability: {prediction_proba:.2f}')

if prediction_proba > 0.5:
    st.write('The customer is likely to churn.')
else:
    st.write('The customer is not likely to churn.')