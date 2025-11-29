import streamlit as st
import requests
import pandas as pd
import numpy as np
import os

# SENIOR UPGRADE: 
# If running in Docker, use the internal network name 'http://api:8000'
# If running locally, use 'http://127.0.0.1:8000'
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Bolt Pricing Simulator", layout="wide")

st.title("⚡ Bolt-Style Dynamic Pricing Engine")
st.markdown("### H3 Spatial Indexing & Demand Prediction")

# Debugging Helper (Optional - helps you see where it's trying to connect)
with st.expander("Debug Connection Info"):
    st.write(f"Connecting to API at: `{API_URL}`")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Request a Ride")
    st.info("Simulating user location in Tallinn, Estonia")
    
    # Inputs
    input_lat = st.number_input("Latitude", value=59.4370, format="%.4f")
    input_lon = st.number_input("Longitude", value=24.7536, format="%.4f")
    
    if st.button("Check Price", type="primary"):
        try:
            payload = {"lat": input_lat, "lon": input_lon}
            # Use the dynamic URL
            response = requests.post(f"{API_URL}/predict_fare", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Metric Cards
                st.divider()
                m1, m2 = st.columns(2)
                m1.metric("Dynamic Price", f"€{data['final_price']}", delta=f"{data['surge_multiplier']}x Surge")
                m2.metric("Drivers Nearby", data['available_drivers'])
                
                st.write(f"**H3 Hex ID:** `{data['hex_id']}`")
                st.write(f"**Predicted Demand:** {data['predicted_demand']} req/hr")
                
                if data['surge_multiplier'] > 1.5:
                    st.error("🔥 High Demand Area!")
                else:
                    st.success("✅ Standard Pricing Active")
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection Error: {e}")

with col2:
    st.header("Live Demand Map")
    
    # Fetch Visualization Data
    try:
        # Use the dynamic URL
        viz_response = requests.get(f"{API_URL}/heat_map_data")
        if viz_response.status_code == 200:
            viz_data = pd.DataFrame(viz_response.json())
            
            # STANDARD MAP
            st.map(viz_data, latitude='lat', longitude='lon', size=20, color='#FF4B4B')
            st.caption("Red dots represent ride request clusters in the last hour.")
            
    except Exception as e:
        st.warning(f"Could not connect to Backend at {API_URL}. Is the API container running?")

st.markdown("---")
st.caption("Architecture: Docker Microservices (Streamlit + FastAPI)")