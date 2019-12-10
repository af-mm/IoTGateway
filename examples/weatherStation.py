import paho.mqtt.client as mqtt
import time

HOST = 'localhost'
PORT = 20021
TOPIC = '/room/weather_station/request'

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))

client = mqtt.Client();
client.on_connect = on_connect

client.connect(HOST, PORT, 60)

i = 0
while True:
    msg = 'lol_{}'.format(i)
    i = i + 1
    client.publish(TOPIC, 'get')
    client.loop(0.001)
    print(msg)
    time.sleep(30)
