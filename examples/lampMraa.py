import paho.mqtt.client as mqtt
import mraa

HOST = '192.168.1.53'
PORT = 1024
TOPIC = '001/light'
SWITCH_PIN = 0
LAMP_PIN = 8

SWITCH = mraa.Aio(SWITCH_PIN)
LAMP = mraa.Gpio(LAMP_PIN)
LAMP.dir(mraa.DIR_OUT)

LAMP.write(0)
switchState = 0

def turnLamp(newState):
    global LAMP
    global switchState

    if newState:
        LAMP.write(1)
        switchState = 1
    else:
        LAMP.write(0)
        switchState = 0

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))

    client.subscribe([(TOPIC, 0)])

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf8')

    print('{} : {}'.format(topic, payload))

    if topic == TOPIC:
        if payload == 'turn on':
            turnLamp(1)
            client.publish(TOPIC, 'on')
            print('Lamp turned on')
        elif payload == 'turn off':
            turnLamp(0)
            client.publish(TOPIC, 'off')
            print('Lamp turned on')



client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)

btnState = 0
while True:
    if SWITCH.read() > 1000:
        if btnState == 0:
            if switchState == 0:
                turnLamp(1)
                client.publish(TOPIC, 'on')
                print('lamp triggered on')
            else:
                turnLamp(0)
                client.publish(TOPIC, 'off')
                print('lamp triggered off')
            btnState = 1
    else:
        btnState = 0
    client.loop(0.1)
