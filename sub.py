import paho.mqtt.client as paho
import cv2
from paho import mqtt
import base64
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv()



# Config 
mqtt_topic = "test_cam"

# Connect
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

# On message
def on_message(client, userdata, msg):
    print("Received message")
    print("Size of message", len(msg.payload))

    # Decode base64
    jpg_original = base64.b64decode(msg.payload)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    # Resize
    scale_percent = 200
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height))
    
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
   

# Init MQTT Client
client = paho.Client()


client.on_connect = on_connect
client.on_message = on_message


# Set ssl protocol to TLSv1_2 if using HiveMQ Cloud
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(os.getenv("UBUNTU_USER"), os.getenv("UBUNTU_PASSWORD"))
#connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(os.getenv("UBUNTU_CLUSTER"),int(os.getenv("UBUNTU_PORT")))

# Listen to the topic
client.loop_forever()
