import random
import time
import csv

# Create CSV file and add headers
with open("sensor_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Reading", "Temperature", "Humidity", "CO2"])

# Function to simulate sensor data
def get_sensor_data():
    temperature = random.uniform(18, 35)
    humidity = random.uniform(30, 80)
    co2 = random.uniform(300, 1200)
    return temperature, humidity, co2

# Function to check conditions
def check_conditions(temp, hum, co2):
    if temp > 30:
        print("⚠️ High Temperature!")
    if hum > 70:
        print("⚠️ High Humidity!")
    if co2 > 1000:
        print("⚠️ Poor Air Quality!")

# Main loop
for i in range(20):  # increased readings
    temp, hum, co2 = get_sensor_data()

    print(f"\nReading {i+1}:")
    print(f"Temperature: {temp:.2f} °C")
    print(f"Humidity: {hum:.2f} %")
    print(f"CO2: {co2:.2f} ppm")

    check_conditions(temp, hum, co2)

    # Save to CSV
    with open("sensor_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([i+1, temp, hum, co2])

    time.sleep(1)