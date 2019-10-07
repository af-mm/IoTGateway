import paho.mqtt.client as mqtt
import time

ID_DOOR_DEVICE = '0000000001'
DOOR_STATE = '{}/state'.format(ID_DOOR_DEVICE)

ID_KETTLE_DEVICE = '0000000002'
KETTLE_STATE = '{}/state'.format(ID_KETTLE_DEVICE)

forwardMap = {DOOR_STATE : 'kitchen/door/state', KETTLE_STATE : 'kitchen/kettle/state'}
backwardMap = {'kitchen/door/state' : DOOR_STATE, 'kitchen/kettle/state' : KETTLE_STATE}


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
clientLeft.connect('localhost', 1024, 60)

clientRight = mqtt.Client();
clientRight.on_connect = on_connect
clientRight.on_message = on_message_backward
clientRight.connect('localhost', 1025, 60)

while True:
    clientLeft.loop(0.00001)
    clientRight.loop(0.00001)