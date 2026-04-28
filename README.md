# 🏢 Smart Building IoT System – Helix Residences

## 📌 Overview

This project simulates a **multi-domain IoT system** for a smart residential building (Helix Residences).
It monitors environmental conditions, energy usage, and security in real time using a combination of hardware simulation (Wokwi) and a web-based dashboard (Streamlit).

---

## 🚀 Features

* 🌡️ Environmental Monitoring (Temperature, Humidity, PM2.5)
* ⚡ Energy Monitoring (simulated using LDR)
* 🔐 Security Monitoring (PIR motion detection)
* 🔔 Real-time Alerts (LED + Buzzer)
* 📊 Live Dashboard with charts and alerts
* 🧠 Multi-domain IoT architecture

---

## 🧱 Technologies Used

* Python
* Streamlit
* Pandas
* Altair (for charts)
* Wokwi (IoT simulation)

---

## ▶️ How to Run the Dashboard

### 1. Install dependencies

```bash
pip install streamlit pandas altair streamlit-autorefresh
```

### 2. Run the dashboard

```bash
streamlit run dashboard_web.py
```

### 3. Open in browser

If it doesn't open automatically, go to:

```
http://localhost:8501
```

---

---

## 🔌 Wokwi Hardware Setup

### Sensors:

* Potentiometer → Environmental data
* LDR → Energy usage
* PIR → Security

### Actuators:

* LED → Visual alert
* Buzzer → Sound alert

---

## 📊 System Architecture

The system consists of:

* **Sensors (Wokwi simulation)** → Data collection
* **ESP32** → Edge processing
* **Python system** → Data processing & logic
* **Streamlit dashboard** → Visualization

---

## 🧾 Notes

* Sensor values are simulated for demonstration purposes
* The system represents a real-world IoT smart building setup
* Additional sensors can be integrated in future work

---

## 👤 Author

Sachin Adhikari
