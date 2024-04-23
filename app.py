from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import base64
import paho.mqtt.client as paho
from paho import mqtt
from kivy.clock import mainthread       

from dotenv import load_dotenv
import os

load_dotenv()




class CameraApp(App):
    def build(self):
        self.layout = BoxLayout()
        self.texture = Texture.create(size=(1, 1))  # Tạo một texture rỗng ban đầu
        self.image = Image(texture=self.texture)
        self.layout.add_widget(self.image)

        self.client = paho.Client()
        return self.layout
       
    def on_start(self):
        self.client.on_message = self.on_message
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(os.getenv("USER"), os.getenv("PASSWORD"))
        self.client.connect(os.getenv("CLUSTER"),int(os.getenv("PORT")))
        self.client.subscribe('test_cam')
        Clock.schedule_interval(self.loop , 1.0 / 30.0)

    def loop(self, dt):
        self.client.loop(0.1)

    # On message
    @mainthread
    def on_message(self,client, userdata, msg):
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
        img = cv2.flip(img, 0)

        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture.blit_buffer(img.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

        
            

if __name__ == '__main__':
    CameraApp().run()
