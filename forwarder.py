import paho.mqtt.client as mqtt
import time
import config

forwardMap = {}
backwardMap = {}

for key in config.MAPPING:
    forwardMap[key] = config.MAPPING[key]
    backwardMap[config.MAPPING[key]] = key
    
print('forwardMap = {}'.format(forwardMap))
print('backwardMap = {}'.format(backwardMap))


CACHE = set()

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([('#', 0)])
    
def on_message_forward(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    global forwardMap
    global clientRight
    global CACHE
    
    if topic in forwardMap:
        if topic in CACHE:
            CACHE.remove(topic)
        else:
            CACHE.add(forwardMap[topic])
            clientRight.publish(forwardMap[topic], payload)
            print('{}:{} -> {}:{}'.format(topic, payload, forwardMap[topic], payload))
    
def on_message_backward(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    global backwardMap
    global clientLeft
    global CACHE
    
    if topic in backwardMap:
        if topic in CACHE:
            CACHE.remove(topic)
        else:
            CACHE.add(backwardMap[topic])
            clientLeft.publish(backwardMap[topic], payload)
            print('{}:{} -> {}:{}'.format(topic, payload, backwardMap[topic], payload))

clientLeft = mqtt.Client();
clientLeft.on_connect = on_connect
clientLeft.on_message = on_message_forward
clientLeft.connect(config.EXTERNAL_MQTT_BROKER['host'], config.EXTERNAL_MQTT_BROKER['port'], 60)

clientRight = mqtt.Client();
clientRight.on_connect = on_connect
clientRight.on_message = on_message_backward
clientRight.connect(config.INTERNAL_MQTT_BROKER['host'], config.INTERNAL_MQTT_BROKER['port'], 60)

while True:
    clientLeft.loop(0.00001)
    clientRight.loop(0.00001)