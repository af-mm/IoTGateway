import paho.mqtt.client as mqtt

HOST = 'localhost'
PORT = 20021
STATE = '/room/allLights'

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([(STATE, 0)])
    
def on_message(client, userdata, message):
    #global TS
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    if topic == STATE:
        if payload == 'turn on':
            for i in range(4):
                client.publish('/room/small_lamp{}'.format(i + 1), 'turn on')
            client.publish('/room/light1', '100')
            client.publish('/room/light2', '100')
            client.publish('/room/ss1', 'on')
            client.publish('/room/ss2', 'on')
        elif payload == 'turn off':
            for i in range(4):
                client.publish('/room/small_lamp{}'.format(i + 1), 'turn off')
            client.publish('/room/light1', '0')
            client.publish('/room/light2', '0')
            client.publish('/room/ss1', 'off')
            client.publish('/room/ss2', 'off')


client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)

client.loop_forever()
