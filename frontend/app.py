import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Product Store Sales Prediction
st.title("Product Store Sales Prediction App")
st.write("Predict the **Total Product Store Sales** based on product details and store characteristics.")
st.write("Adjust the inputs below to calculate a prediction from the API.")

# Form Layout splits inputs into Product details and Store details
st.header("🛒 Product Attributes")
col1, col2 = st.columns(2)

with col1:
    product_type = st.selectbox(
        "Product Type", 
        ["Frozen Foods", "Dairy", "Canned", "Baking Goods", "Health and Hygiene", "Meat", "Snack Foods"]
    )
    product_mrp = st.slider("Product Maximum Retail Price (MRP)", 10.0, 500.0, 150.0, 0.01)
    product_weight = st.slider("Product Weight", 1.0, 50.0, 13.0, 0.01)

with col2:
    product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    product_area = st.slider("Product Allocated Area (Ratio)", 0.001, 0.300, 0.050, 0.001)

st.header("🏪 Store Attributes")
col3, col4 = st.columns(2)

with col3:
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])

with col4:
    store_city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_year = st.number_input("Store Establishment Year", min_value=1950, max_value=2026, value=1999, step=1)

# Create JSON payload matching the target columns
input_data = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar,
    'Product_Allocated_Area': product_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Establishment_Year': store_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_city,
    'Store_Type': store_type
}

# Single Prediction Request
if st.button("Predict Sales", type='primary'):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/sales",
            json=input_data
        )

        if response.status_code == 200:
            result = response.json()
            predicted_sales = result["Predicted_Sales_Total"]
            st.success(f"📈 **Predicted Total Store Sales:** ${predicted_sales:,.2f}")
        else:
            st.error(f"Error in API request. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Please verify that the server container is up and running.")

# Batch Prediction
st.markdown("---")
st.subheader("📊 Batch Prediction")
file = st.file_uploader("Upload CSV file containing product rows", type=["csv"])

if file is not None:
    if st.button("Predict for Batch", type='primary'):
        # Reset file pointer to ensure file is read cleanly from the beginning
        file.seek(0)
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/salesbatch",
                files={"file": (file.name, file.getvalue(), "text/csv")}
            )

            if response.status_code == 200:
                result = response.json()
                st.header("Batch Prediction Results")
                
                # Turn JSON list response into a highly scannable DataFrame view
                if isinstance(result, list) or isinstance(result, dict):
                    st.dataframe(pd.DataFrame(result))
                else:
                    st.write(result)
            else:
                st.error(f"Error in Batch API request. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server.")
