# Homomorphic Encryption ML Demo

## 1. Methodology
![Methodology Diagram](https://mermaid.ink/img/pako:eNp1kc1uwyAQhF9l5VOkOnf8ANF9SJ1TT1UlDtjEVrAxMk7TKO-OcZrGP1Vyw-zON8tidhAGQ8gV7GE3BeuIXGSaXaNV25Qb4bsJqSeXsXdIgYRVn_KCjInVPE3P-jDO8YP8RN6i_Ko-8CuoWq939wfSocw56UdXsuiq6xR6MMhOutfdqxr98BYVqTAPR-csuo3CjLwm5REj2iA4UZkkqB91VV1XNdrlfcdpgldYL8WDYN0v56NadLQUS_hbYoV1hxJNoi9nZM6qMpNjvStSYtnm3XijtK8rQwLbsqm2TTM7wyHCFnyTguj9FUJ57_eBPIUQ2OsH-PH_7A?type=png)

## 2. Description
- **Purpose**: Privacy-preserving salary prediction using homomorphic encryption
- **Models**: Linear Regression
- **Accuracy**: High accuracy on salary prediction while maintaining data privacy
- **Other Information**: Demonstrates real-world application of homomorphic encryption in machine learning

## 3. Input / Output

| Input Data | Processing Step | Encrypted Result | Final Output |
|------------|----------------|-----------------|--------------|
| Age, Healthy Eating, Active Lifestyle, Gender | Encryption | Encrypted values | Predicted Salary |
| Customer Data | Model Calculation | Encrypted prediction | Decrypted Salary |
| Private Information | Privacy-Preserving Computation | Secure Transfer | Usable Results |



## 5. Application Interface
![Interface Screenshot](image.png)

## 6. Implementation Details

### Components:
1. **Customer Side (cust.py)**:
   - Generates and stores private/public key pair
   - Encrypts sensitive data
   - Decrypts the result after model processing

2. **ML Company Side (servercalc.py & linmodel.py)**:
   - Receives encrypted data from customer
   - Processes data using ML model weights
   - Returns encrypted prediction
   - Never sees the actual data values

3. **Interactive Demo (app.py)**:
   - Streamlit application for visualization
   - Interactive data input
   - Real-time encryption demonstration
   - Visual representation of results

## 7. How to Run
```bash
# Install requirements
pip install phe pandas numpy scikit-learn streamlit matplotlib seaborn

# Run the Streamlit application
streamlit run app.py
```

## 8. Security Benefits
- Data remains encrypted during entire prediction process
- Model owner never sees sensitive input data
- Data owner never sees the internal model parameters
- Provides privacy while maintaining utility
