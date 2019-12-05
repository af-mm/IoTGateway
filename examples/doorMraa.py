import paho.mqtt.client as mqtt
import mraa

HOST = '192.168.1.53'
PORT = 1024
TOPIC = '002/state'
GERKON_PIN = 0

GERKON = mraa.Aio(GERKON_PIN)

gerkonLastState = -1;

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
client = mqtt.Client();
client.on_connect = on_connect

client.connect(HOST, PORT, 60)

while True:
    v = GERKON.read()
    if v > 512:
        v = 1
    else:
        v = 0
    if v != gerkonLastState:
        gerkonLastState = v
        if v:
            client.publish(TOPIC, 'opened')
            print('opened')
        else:
            client.publish(TOPIC, 'closed')
            print('closed')
    client.loop(0.1)
