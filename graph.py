import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("sensor_data.csv")

# Plot Temperature
plt.figure()
plt.plot(data["Reading"], data["Temperature"])
plt.title("Temperature Over Time")
plt.xlabel("Reading")
plt.ylabel("Temperature (°C)")
plt.show()

# Plot Humidity
plt.figure()
plt.plot(data["Reading"], data["Humidity"])
plt.title("Humidity Over Time")
plt.xlabel("Reading")
plt.ylabel("Humidity (%)")
plt.show()

# Plot CO2
plt.figure()
plt.plot(data["Reading"], data["CO2"])
plt.title("CO2 Levels Over Time")
plt.xlabel("Reading")
plt.ylabel("CO2 (ppm)")
plt.show()