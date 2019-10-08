import paho.mqtt.client as mqtt
from config import EXTERNAL_MQTT_BROKER

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([('0000000001/state', 0), ])
    
def on_message(client, userdata, message):
    global TS
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    if topic == '0000000001/state':
        if payload == 'opened':
            client.publish('0000000002/state', 'on')
            print('door opened -> kettle turns on')

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect(EXTERNAL_MQTT_BROKER['host'], EXTERNAL_MQTT_BROKER['port'], 60)

client.loop_forever()