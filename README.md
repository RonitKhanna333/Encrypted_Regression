# Homomorphic Encryption ML Demo

## 1. Methodology
![](https://mermaid.ink/img/pako:eNptkMtuwyAQRX9lxCpS7Vp-YOQ-pO5cN5UYBoNrI4QZYZyu_PeCnTYPdTkzw72cGbgB1_YgGL7gdrDCEVXnSJpiU1WNcH0gGpybHNghO5QX-YnqWuo8jc_l7pjVBwUHMRCqr_KEX4rOvdrWGdqLlOrTGKNtR51i92wQ03Avu1c5huabpFjCvT9YGcQlI8nIGWUge8QeLCUmrAX95aq4zaxW43vG6YdXWC_ZPXLubhn5N7NgXJ9Nfw2SRwpV_eNW6Uyqcl6LS1JMKeMSosBZZLQUmhEXhRJpKVLeLuEXMduS3w?type=png)

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
