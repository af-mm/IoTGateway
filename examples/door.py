import paho.mqtt.client as mqtt
import time

HOST = ''
PORT = 0
ID_DOOR_DEVICE = '0000000001'
DOOR_STATE = '0000000001/state'.format(ID_DOOR_DEVICE)

ID_KETTLE_DEVICE = '0000000002'
KETTLE_STATE = '{}/state'.format(ID_KETTLE_DEVICE)

TS = time.time()

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([(DOOR_STATE, 0), (KETTLE_STATE, 0)])
    
def on_message(client, userdata, message):
    global TS
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    if topic == DOOR_STATE:
        TS = time.time()
    elif topic == KETTLE_STATE:
        if payload == 'off':
            print('delay = {} sec'.format(time.time() - TS))

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)

client.loop_forever()