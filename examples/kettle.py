import paho.mqtt.client as mqtt
import time

HOST = ''
PORT = 0
ID_KETTLE_DEVICE = '0000000002'
KETTLE_STATE = '{}/state'.format(ID_KETTLE_DEVICE)

TS = time.time()

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([(KETTLE_STATE, 0)])
    
def on_message(client, userdata, message):
    global TS
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    if topic == KETTLE_STATE:
        if payload == 'on':
            client.publish(KETTLE_STATE, 'off')

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)

client.loop_forever()