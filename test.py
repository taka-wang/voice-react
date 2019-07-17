import paho.mqtt.client as mqtt
from pixel_ring import pixel_ring
import time

HOST = '127.0.0.1'
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    # Subscribe to the hotword detected topic
    client.subscribe("hermes/hotword/default/detected")

    client.subscribe("hermes/asr/textCaptured")
    # Subscribe to intent topic
    client.subscribe('hermes/intent/#')
    
def on_message(client, userdata, msg):
    if msg.topic == 'hermes/hotword/default/detected':
        print("Hotword detected!")
        pixel_ring.think() # actually listening
    if msg.topic == 'hermes/asr/textCaptured':
        print("Captured")
        pixel_ring.set_color(r=255)
        time.sleep(0.5)
        pixel_ring.off()
    elif msg.topic.startswith('hermes/intent/'):
        print("Intent detected!")
        #pixel_ring.set_color(r=255,g=255)
        pixel_ring.speak()
        time.sleep(1)
        pixel_ring.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

pixel_ring.off()
client.connect(HOST, PORT, 60)
client.loop_forever()

