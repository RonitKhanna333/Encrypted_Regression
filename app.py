import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linmodel import LinModel
import phe as paillier
import json
import os

st.set_page_config(page_title="Homomorphic Encryption ML Demo", layout="wide")

st.title("Salary Prediction with Homomorphic Encryption")
st.markdown("""
This application demonstrates how machine learning can be performed on encrypted data.
The model predicts salary based on age, healthy eating score, active lifestyle score, and gender.
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('employee_data.csv')

df = load_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Data Visualization", "Model Insights", "Encrypted Prediction"])

if page == "Data Visualization":
    st.header("Employee Data Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Sample")
        st.dataframe(df.head(10))
        
        st.subheader("Data Statistics")
        st.dataframe(df.describe())
    
    with col2:
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    
    st.subheader("Feature Distributions")
    col1, col2 = st.columns(2)
    
    with col1:
        feature = st.selectbox("Select Feature", df.columns)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df[feature], kde=True, ax=ax)
        st.pyplot(fig)
    
    with col2:
        x_axis = st.selectbox("X-Axis", df.columns, index=0)
        y_axis = st.selectbox("Y-Axis", df.columns, index=4)  # Default to salary
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue='Gender', ax=ax)
        st.pyplot(fig)

elif page == "Model Insights":
    st.header("Linear Regression Model Insights")
    
    # Get model coefficients
    model = LinModel()
    coefficients = model.getCoef()
    features = df.drop('salary', axis=1).columns
    
    # Display coefficients
    st.subheader("Model Coefficients")
    coef_data = pd.DataFrame({
        'Feature': features,
        'Coefficient': coefficients
    })
    st.dataframe(coef_data)
    
    # Visualize coefficients
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Feature', y='Coefficient', data=coef_data, ax=ax)
    plt.title('Feature Importance')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Get model performance metrics
    _, _, rmse, r_squared = model.getResults()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("RMSE", f"{rmse:.2f}")
    with col2:
        st.metric("R² Score", f"{r_squared:.2f}")

else:  # Encrypted Prediction
    st.header("Encrypted Salary Prediction")
    
    st.markdown("""
    This section demonstrates how to use homomorphic encryption for privacy-preserving predictions.
    
    1. Enter your data
    2. The data will be encrypted
    3. The model will process the encrypted data
    4. Result will be decrypted and displayed
    """)
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", min_value=18, max_value=65, value=30)
            healthy_eating = st.slider("Healthy Eating Score (1-10)", min_value=1, max_value=10, value=5)
        
        with col2:
            active_lifestyle = st.slider("Active Lifestyle Score (1-10)", min_value=1, max_value=10, value=5)
            gender = st.radio("Gender", ["Male", "Female"])
            gender_code = 1 if gender == "Male" else 0
        
        submitted = st.form_submit_button("Predict Salary")
    
    if submitted:
        # Generate keys if they don't exist
        if not os.path.exists('custkeys.json') or os.stat('custkeys.json').st_size == 0:
            public_key, private_key = paillier.generate_paillier_keypair()
            keys = {}
            keys['public_key'] = {'n': public_key.n}
            keys['private_key'] = {'p': private_key.p, 'q': private_key.q}
            with open('custkeys.json', 'w') as file: 
                json.dump(keys, file)
        else:
            with open('custkeys.json', 'r') as file:
                keys = json.load(file)
                public_key = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
                private_key = paillier.PaillierPrivateKey(public_key, keys['private_key']['p'], keys['private_key']['q'])
        
        # Create data array
        data = [age, healthy_eating, active_lifestyle, gender_code]
        
        with st.spinner("Encrypting data..."):
            # Encrypt data
            encrypted_data_list = [public_key.encrypt(x) for x in data]
            encrypted_data = {}
            encrypted_data['public_key'] = {'n': public_key.n}
            encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
            serialized = json.dumps(encrypted_data)
            
            # Save to data.json
            with open('data.json', 'w') as file:
                json.dump(serialized, file)
            
            st.success("Data encrypted and sent to server")
        
        # Calculate prediction (normally this would happen on the server)
        with st.spinner("Server processing encrypted data..."):
            from servercalc import serializeData
            datafile = serializeData()
            with open('answer.json', 'w') as file:
                json.dump(datafile, file)
            
            st.success("Calculation complete")
        
        # Decrypt result
        with st.spinner("Decrypting result..."):
            with open('answer.json', 'r') as file:
                ans = json.load(file)
            answer = json.loads(ans)
            answer_key = paillier.PaillierPublicKey(n=int(answer['pubkey']['n']))
            encrypted_answer = paillier.EncryptedNumber(answer_key, int(answer['values'][0]), int(answer['values'][1]))
            
            if answer_key.n == public_key.n:
                salary = private_key.decrypt(encrypted_answer)
                st.success(f"Decryption successful!")
                
                st.balloons()
                st.header(f"Predicted Salary: ${salary:.2f}")
                
                # Show comparison to average
                avg_salary = df['salary'].mean()
                if salary > avg_salary:
                    percent_above = ((salary - avg_salary) / avg_salary) * 100
                    st.info(f"This is {percent_above:.1f}% above the average salary of ${avg_salary:.2f}")
                else:
                    percent_below = ((avg_salary - salary) / avg_salary) * 100
                    st.info(f"This is {percent_below:.1f}% below the average salary of ${avg_salary:.2f}")
            else:
                st.error("Error: Key mismatch. Cannot decrypt the result.")

# Footer
st.markdown("---")
st.markdown("**Homomorphic Encryption Demo** - Privacy-preserving machine learning")
