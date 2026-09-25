import streamlit as st
import pandas as pd
import joblib

# Initialize Flask app
app = Flask("SuperKart Predictor ")

# Load the trained Boston housing model
model = joblib.load("SuperKart.joblib")
# Load the trained regression model
def load_model():
    # Replace with your actual model file path when ready
    try:
        return joblib.load("product_sales_model_v1_0.joblib")
    except FileNotFoundError:
        # Fallback dummy model for testing UI layout if file doesn't exist yet
        class DummyModel:
            def predict(self, df):
                # Simple mock prediction logic based on MRP and Product Allocated Area
                return df['Product_MRP'].values * 25.0 - (df['Product_Allocated_Area'].values * 1000)
        return DummyModel()

model = load_model()

# Streamlit UI for Product Store Sales Prediction
st.title("Product Store Sales Prediction App")
st.write("Predict the **Total Product Store Sales** based on product details and store characteristics.")
st.write("Adjust the inputs below to calculate a prediction.")

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

# Package data into a DataFrame format matching your training columns
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar,
    'Product_Allocated_Area': product_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Establishment_Year': store_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_city,
    'Store_Type': store_type
}])

# Predict Button
st.markdown("---")
if st.button("Predict Total Sales", type="primary"):
    predicted_sales = model.predict(input_data)
    
    # Handle single element array outputs gracefully
    if hasattr(predicted_sales, '__len__'):
        final_sales = float(predicted_sales[0])
    else:
        final_sales = float(predicted_sales)
        
    st.success(f"📈 **Predicted Total Store Sales:** ${final_sales:,.2f}")
