#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT setup
BROKER = "localhost"
PORT = 1883
TOPICS = ["iesl/wellhead/pressure", "iesl/wellhead/temperature", "iesl/wellhead/flow"]

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def generate_sensor_data():
    # Simulating a wellhead in an oil field
    pressure = round(random.uniform(800, 1200), 2)  # psi
    temperature = round(random.uniform(60, 95), 1)  # Fahrenheit
    flow_rate = round(random.uniform(200, 600), 2)  # barrels per day
    
    return {
        "iesl/wellhead/pressure": pressure,
        "iesl/wellhead/temperature": temperature,
        "iesl/wellhead/flow": flow_rate
    }

print("Starting IESL wellhead sensor simulator... Press Ctrl+C to stop")
try:
    while True:
        data = generate_sensor_data()
        timestamp = int(time.time())
        
        for topic, value in data.items():
            payload = {
                "value": value,
                "timestamp": timestamp,
                "wellhead_id": "WH-03",
                "location": "Field_Alpha"
            }
            client.publish(topic, json.dumps(payload))
            print(f"Published to {topic}: {value}")
        
        time.sleep(5)  # Send every 5 seconds
except KeyboardInterrupt:
    print("\nStopping simulator")
    client.disconnect()
