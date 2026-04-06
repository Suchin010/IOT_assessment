import streamlit as st
import random
import time
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

# ---- STYLE ----
st.markdown("""
<style>
.stApp {
    background-color: #111827;
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Smart Building Dashboard")

# ---- SESSION STATE ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Temp", "Humidity", "PM25"])
    st.session_state.start_time = time.time()

    # Initial realistic values
    st.session_state.temp = 25
    st.session_state.hum = 50
    st.session_state.pm25 = 40

# ---- SETTINGS ----
UPDATE_INTERVAL = 2
WINDOW = 60

# ---- REALISTIC SENSOR SIMULATION ----
st.session_state.temp += random.uniform(-0.3, 0.3)
st.session_state.hum += random.uniform(-1, 1)
st.session_state.pm25 += random.uniform(-5, 5)

# Clamp values
st.session_state.temp = max(18, min(35, st.session_state.temp))
st.session_state.hum = max(30, min(80, st.session_state.hum))
st.session_state.pm25 = max(10, min(150, st.session_state.pm25))

temp = st.session_state.temp
hum = st.session_state.hum
pm25 = st.session_state.pm25

current_time = round(time.time() - st.session_state.start_time, 1)

# ---- STORE DATA ----
new_row = {
    "Time": current_time,
    "Temp": temp,
    "Humidity": hum,
    "PM25": pm25
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
)

# ---- KEEP LAST 60 SEC ----
st.session_state.data = st.session_state.data[
    st.session_state.data["Time"] >= (current_time - WINDOW)
]

# ---- METRICS ----
col1, col2, col3 = st.columns(3)

col1.metric("🌡️ Temperature", f"{temp:.1f} °C")
col2.metric("💧 Humidity", f"{hum:.1f} %")
col3.metric("🌫️ PM2.5", f"{pm25:.1f} µg/m³")

# ---- ALERTS ----
if temp > 30:
    st.error("🔥 High Temperature Detected!")

elif hum > 70:
    st.warning("💧 High Humidity Detected!")

elif pm25 > 100:
    st.error("🌫️ Poor Air Quality!")

else:
    st.success("✅ Environment Normal")

data = st.session_state.data

# ---- CHARTS ----
col1, col2, col3 = st.columns(3)

# Temperature chart
with col1:
    st.subheader("Temperature")
    temp_chart = alt.Chart(data).mark_line().encode(
        x=alt.X('Time', title='Time (s)'),
        y=alt.Y('Temp', scale=alt.Scale(domain=[
            data["Temp"].min() - 1,
            data["Temp"].max() + 1
        ]), title='°C')
    ).properties(height=250)

    st.altair_chart(temp_chart, use_container_width=True)

# Humidity chart
with col2:
    st.subheader("Humidity")
    hum_chart = alt.Chart(data).mark_line().encode(
        x='Time',
        y=alt.Y('Humidity', scale=alt.Scale(domain=[
            data["Humidity"].min() - 5,
            data["Humidity"].max() + 5
        ]), title='%')
    ).properties(height=250)

    st.altair_chart(hum_chart, use_container_width=True)

# PM2.5 chart
with col3:
    st.subheader("PM2.5")
    pm_chart = alt.Chart(data).mark_line().encode(
        x='Time',
        y=alt.Y('PM25', scale=alt.Scale(domain=[
            data["PM25"].min() - 10,
            data["PM25"].max() + 10
        ]), title='µg/m³')
    ).properties(height=250)

    st.altair_chart(pm_chart, use_container_width=True)

# ---- REFRESH ----
time.sleep(UPDATE_INTERVAL)
st.rerun()