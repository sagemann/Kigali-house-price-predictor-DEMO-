import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('kigali_house_model.pkl')

st.title("ABC company Price Predictor")
st.markdown("Enter house details to get a fair price range")

# Input form
neighborhood = st.selectbox("Neighborhood", 
                            ["Kiyovu", "Nyarutarama", "Kimihurura", "Kimironko", 
                             "Nyamirambo", "Kacyiru", "Remera", "Gisozi"])

plot_size = st.number_input("Plot Size (sqm)", min_value=100.0, max_value=2000.0, value=500.0, step=50.0)
bedrooms = st.slider("Bedrooms", 1, 8, 4)
bathrooms = st.slider("Bathrooms", 1, 6, 3)

if st.button("Predict Price"):
    # Make DataFrame
    input_data = pd.DataFrame([{
        "neighborhood": neighborhood,
        "plot_size_sqm": plot_size,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms
    }])

    pred = model.predict(input_data)[0]
    low = pred * 0.9
    high = pred * 1.1

    st.success(f"Predicted Price: **{round(pred, 1)} million RWF**")
    st.info(f"Fair Range: {round(low, 1)} - {round(high, 1)} million RWF")

# Footer
st.markdown("---")
st.caption("Built by NOCTURNALS – ABC Platform Fair Pricing Tool")