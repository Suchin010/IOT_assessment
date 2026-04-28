import streamlit as st
import random
import time
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Dashboard Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)
window = st.sidebar.slider("Time Window (seconds)", 30, 120, 60)

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=refresh_rate * 1000, key="refresh")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #22c55e;
}

.metric-label {
    font-size: 14px;
    color: #94a3b8;
}

.live {
    color: red;
    font-weight: bold;
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([6,1])
with col1:
    st.title("🏢 Smart Building Dashboard")
with col2:
    st.markdown("<div class='live'>● LIVE</div>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time","Temp","Humidity","PM25","Energy","Intrusion"])
    st.session_state.start_time = time.time()
    st.session_state.temp = 25
    st.session_state.hum = 50
    st.session_state.pm25 = 40

# ---------------- DATA SIMULATION ----------------
st.session_state.temp += random.uniform(-0.3, 0.3)
st.session_state.hum += random.uniform(-1, 1)
st.session_state.pm25 += random.uniform(-5, 5)

st.session_state.temp = max(18, min(35, st.session_state.temp))
st.session_state.hum = max(30, min(80, st.session_state.hum))
st.session_state.pm25 = max(10, min(150, st.session_state.pm25))

temp = st.session_state.temp
hum = st.session_state.hum
pm25 = st.session_state.pm25

energy = random.uniform(100, 500)
intrusion = random.choice([0,1])

current_time = round(time.time() - st.session_state.start_time, 1)

# ---------------- STORE ----------------
new_row = {
    "Time": current_time,
    "Temp": temp,
    "Humidity": hum,
    "PM25": pm25,
    "Energy": energy,
    "Intrusion": intrusion
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
)

data = st.session_state.data[
    st.session_state.data["Time"] >= (current_time - window)
]

# ---------------- CARDS ----------------
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='card'><div class='metric-label'>Temperature</div><div class='metric-value'>{temp:.1f}°C</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><div class='metric-label'>Humidity</div><div class='metric-value'>{hum:.1f}%</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><div class='metric-label'>PM2.5</div><div class='metric-value'>{pm25:.1f}</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><div class='metric-label'>Energy</div><div class='metric-value'>{energy:.0f}</div></div>", unsafe_allow_html=True)

# ---------------- ALERTS ----------------
alerts = []

if temp > 30:
    alerts.append("🔥 High Temperature")

if hum > 70 or pm25 > 100:
    alerts.append("🌬️ Poor Air Quality")

if energy > 400:
    alerts.append("⚡ High Energy Usage")

if intrusion == 1:
    alerts.append("🚨 Intrusion Detected")

if alerts:
    for a in alerts:
        st.error(a)
else:
    st.success("✅ All Systems Normal")

# ---------------- TAB SELECTION (FIXED) ----------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Environment"

selected_tab = st.radio(
    "",
    ["🌡️ Environment", "⚡ Energy", "🔐 Security"],
    horizontal=True
)

# ---------------- ENVIRONMENT ----------------
if selected_tab == "🌡️ Environment":
    st.subheader("Environmental Trends")

    ec1, ec2, ec3 = st.columns(3)

    ec1.altair_chart(alt.Chart(data).mark_line(color="red").encode(x='Time', y='Temp'), use_container_width=True)
    ec2.altair_chart(alt.Chart(data).mark_line(color="blue").encode(x='Time', y='Humidity'), use_container_width=True)
    ec3.altair_chart(alt.Chart(data).mark_line(color="orange").encode(x='Time', y='PM25'), use_container_width=True)

# ---------------- ENERGY ----------------
elif selected_tab == "⚡ Energy":
    st.subheader("Energy Usage")

    st.altair_chart(
        alt.Chart(data).mark_line(color="yellow").encode(x='Time', y='Energy'),
        use_container_width=True
    )

# ---------------- SECURITY ----------------
elif selected_tab == "🔐 Security":
    st.subheader("Security Activity")

    st.altair_chart(
        alt.Chart(data).mark_bar(color="purple").encode(x='Time', y='Intrusion'),
        use_container_width=True
    )

# ---------------- TABLE ----------------
st.markdown("---")
st.subheader("📄 Live Sensor Data")

st.dataframe(data.tail(20), use_container_width=True, height=250)