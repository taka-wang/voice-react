# encoding: utf-8
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
from pixel_ring import pixel_ring
import time
import json
import sys
import logging

# Setup logger
logging.basicConfig(stream=sys.stderr, format='%(levelname)7s: %(message)s')
logger = logging.getLogger('Handler')
logger.setLevel(logging.INFO)

# MQTT client to connect to the bus
client = mqtt.Client()
HOST = "localhost"
PORT = 1883

# Snips topcis
HOTWORD_DETECTED = "hermes/hotword/default/detected"
TEXT_CAPTURED = "hermes/asr/textCaptured"
ALL_INTENTS = "hermes/intent/#"

# Subscribe to the important messages
def on_connect(client, userdata, flags, rc):
    logger.info("Connected to {0} with result code {1}".format(HOST, rc))
    # Subscribe to the hotword detected topic
    client.subscribe(HOTWORD_DETECTED)
    # Subscribe to the text command captured topic
    client.subscribe(TEXT_CAPTURED)
    # Subscribe to intent topic
    client.subscribe('hermes/intent/#')

# Process a message as it arrives
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    logger.debug("Topic:{0}, Payload:{1}".format(msg.topic, payload))
    if msg.topic == 'hermes/hotword/default/detected':
        logger.info("Hotword detected!")
        pixel_ring.think() # actually listening
    elif msg.topic == 'hermes/asr/textCaptured':
        logger.info("Command captured! [{0}]".format(msg.topic))
        pixel_ring.set_color(r=200)
        time.sleep(0.5)
        pixel_ring.off()
    elif msg.topic == 'hermes/intent/taka-wang:AutoRun':
        logger.info("Intent topic: [{0}]".format(msg.topic))
        pixel_ring.set_color(r=204,g=46,b=250)
        time.sleep(1)
        pixel_ring.off()
    elif msg.topic == 'hermes/intent/taka-wang:Stop':
        logger.info("Intent topic: [{0}]".format(msg.topic))
        pixel_ring.set_color(g=100)
        time.sleep(1)
        pixel_ring.off()
    elif msg.topic == 'hermes/intent/taka-wang:OpenTheDoor':
        logger.info("Intent topic: [{0}]".format(msg.topic))
        pixel_ring.set_color(g=255)
        time.sleep(1)
        pixel_ring.off()
    elif msg.topic == 'hermes/intent/taka-wang:CloseTheDoor':
        logger.info("Intent topic: [{0}]".format(msg.topic))
        pixel_ring.set_color(r=200,g=133)
        time.sleep(1)
        pixel_ring.off()        
    elif msg.topic.startswith('hermes/intent/'):
        logger.info("Intent topic: [{0}]".format(msg.topic))
        pixel_ring.set_color(r=255,g=255)
        time.sleep(1)
        pixel_ring.off()

if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    pixel_ring.off() # turn off ring
    client.loop_forever()