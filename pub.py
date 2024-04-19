import paho.mqtt.client as mqtt
import time
import cv2
import random

# Config
mqtt_broker = "127.0.0.1"
mqtt_port = 1883
mqtt_topic = "test_cam"

client = mqtt.Client()

# Connect to broker
client.connect(mqtt_broker, mqtt_port)

# Webcam
webcam = cv2.VideoCapture(0)

while True:
    # Read frame từ webcam
    ret, frame = webcam.read()

    # Convert frame to binary
    _, img_encoded = cv2.imencode('.jpg', frame)
    message = img_encoded.tobytes()

    # Send message
    client.publish(mqtt_topic, payload=message, qos=0)

    # Delay for reducing CPU usage
    time.sleep(0.1)

# Close MQTT connection and webcam
client.disconnect()
webcam.release()
