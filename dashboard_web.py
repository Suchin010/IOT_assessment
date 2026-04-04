import streamlit as st
import random
import time
import pandas as pd

# Page settings
st.set_page_config(layout="wide")

# Custom dark style
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 Smart Building Dashboard - Helix Residences")

# Initialize session state (prevents resetting)
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Temperature", "Humidity", "CO2"])
    st.session_state.start_time = time.time()

# Layout: 3 columns
col1, col2, col3 = st.columns(3)

# Update settings
UPDATE_INTERVAL = 2  # change to 30 later

# Generate new data
temp = random.uniform(18, 35)
hum = random.uniform(30, 80)
co2 = random.uniform(300, 1200)

current_time = round(time.time() - st.session_state.start_time, 1)

new_row = {
    "Time": current_time,
    "Temperature": temp,
    "Humidity": hum,
    "CO2": co2
}

# Append data
st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
)

# Limit size (keeps it smooth)
st.session_state.data = st.session_state.data.tail(50)

# Display charts side by side
with col1:
    st.subheader("🌡️ Temperature")
    st.line_chart(st.session_state.data.set_index("Time")["Temperature"])

with col2:
    st.subheader("💧 Humidity")
    st.line_chart(st.session_state.data.set_index("Time")["Humidity"])

with col3:
    st.subheader("🌫️ CO₂")
    st.line_chart(st.session_state.data.set_index("Time")["CO2"])

# Auto refresh
time.sleep(UPDATE_INTERVAL)
st.rerun()