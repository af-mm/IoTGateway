import paho.mqtt.client as mqtt
#import time
#from config import EXTERNAL_MQTT_BROKER


STATE = 'room/allLights'

#TS = time.time()

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
                client.publish('0{}/light'.format(i + 1), 'turn on')
            client.publish('L01/light1', '100')
            client.publish('L01/light2', '100')
            client.publish('cmnd/ss1/POWER', 'on')
            client.publish('cmnd/ss2/POWER', 'on')
        elif payload == 'turn off':
            for i in range(4):
                client.publish('0{}/light'.format(i + 1), 'turn off')
            client.publish('L01/light1', '0')
            client.publish('L01/light2', '0')
            client.publish('cmnd/ss1/POWER', 'off')
            client.publish('cmnd/ss2/POWER', 'off')


client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message

client.connect('localhost', 20002, 60)

client.loop_forever()
