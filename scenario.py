import paho.mqtt.client as mqtt
from config import INTERNAL_MQTT_BROKER

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([('kitchen/door/state', 0), ])
    
def on_message(client, userdata, message):
    global TS
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    if topic == 'kitchen/door/state':
        if payload == 'opened':
            client.publish('kitchen/kettle/state', 'on')
            print('door opened -> kettle turns on')

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect(INTERNAL_MQTT_BROKER['host'], INTERNAL_MQTT_BROKER['port'], 60)

client.loop_forever()