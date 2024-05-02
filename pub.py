import paho.mqtt.client as paho
import time
from paho import mqtt
import cv2
import base64
import os
import dotenv

dotenv.load_dotenv()

mqtt_topic = "test_cam"
client = paho.Client()

# Connect to broker
#client.connect(mqtt_broker, mqtt_port)

# Set ssl protocol to TLSv1_2 if using HiveMQ Cloud
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(os.getenv("UBUNTU_USER"), os.getenv("UBUNTU_PASSWORD"))
#connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(os.getenv("UBUNTU_CLUSTER"),int(os.getenv("UBUNTU_PORT")))

print('Connected to MQTT broker')

# Webcam
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    print("Sending...")    
    # Read frame from webcam    
    ret, frame = webcam.read()
    if not ret:
        print("Failed to read frame")
        break

    # Resize frame
    scale_percent = 50  
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    resized_frame = cv2.resize(frame, (width, height))

    # Print size (bytes)
    print('Size of original: ', frame.itemsize * frame.size)
    print('Size of resized: ', resized_frame.itemsize * resized_frame.size)

    # Encode parameters
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  

    # Encode frame to base64
    retval, buffer = cv2.imencode('.jpg', resized_frame, encode_param)
    jpg_as_text = base64.b64encode(buffer)

    print('Size of message', len(jpg_as_text))
    # Publish to MQTT
    client.publish(mqtt_topic, jpg_as_text)

    # Delay
    time.sleep(0.2)

# Close MQTT connection and webcam
client.disconnect()
webcam.release()
