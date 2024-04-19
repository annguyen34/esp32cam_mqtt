import paho.mqtt.client as mqtt
import cv2
import numpy as np

# Config 
mqtt_broker = "127.0.0.1"
mqtt_port = 1883
mqtt_topic = "test_cam"

# Connect
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

# On message
def on_message(client, userdata, msg):
    nparr = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Show image
    cv2.imshow("Video", image)
    cv2.waitKey(1)  

# Init MQTT Client
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Connect to Broker
client.connect(mqtt_broker, mqtt_port, 60)

# Listen to the topic
client.loop_forever()
