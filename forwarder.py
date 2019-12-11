import paho.mqtt.client as mqtt
import psycopg2
from psycopg2.extras import NamedTupleCursor
import hashlib
from config import CFG

def getMessageHash(topic, message):
    return hashlib.md5('{}:{}'.format(topic, message).encode('utf-8')).hexdigest()

CACHE_OF_MESSAGE = set()
EXTERNAL_CACHE = []
INTERNAL_CACHE = []

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([('#', 0)])
    
def on_external_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    global EXTERNAL_CACHE
    
    EXTERNAL_CACHE.append((topic, payload))
    
def on_internal_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    global INTERNAL_CACHE
    
    INTERNAL_CACHE.append((topic, payload))

externalClient = mqtt.Client();
externalClient.on_connect = on_connect
externalClient.on_message = on_external_message
externalClient.username_pw_set(CFG['EXT_MQTT_BROKER']['login'], CFG['EXT_MQTT_BROKER']['password'])
externalClient.connect(CFG['EXT_MQTT_BROKER']['host'], CFG['EXT_MQTT_BROKER']['port'], 60)

internalClient = mqtt.Client();
internalClient.on_connect = on_connect
internalClient.on_message = on_internal_message
internalClient.connect(CFG['INT_MQTT_BROKER']['host'], CFG['INT_MQTT_BROKER']['port'], 60)

selectQuery = 'SELECT topic_to FROM {} WHERE topic_from=%s'
selectExt2IntMappingQuery = selectQuery.format(CFG['db']['table_e2i_mapping'])
selectInt2ExtMappingQuery = selectQuery.format(CFG['db']['table_i2e_mapping'])

dbConn = psycopg2.connect(  host=CFG['db']['host'],
                            port=CFG['db']['port'],
                            dbname=CFG['db']['dbname'],
                            user=CFG['db']['user'],
                            password=CFG['db']['password'])
dbCursor = dbConn.cursor(cursor_factory=NamedTupleCursor)
print('Connected to database')

while True:
    if len(EXTERNAL_CACHE):
        for row in EXTERNAL_CACHE:
            topic, payload = row
            hash = getMessageHash(topic, payload)
            
            if hash in CACHE_OF_MESSAGE:
                CACHE_OF_MESSAGE.remove(hash)
            else:
                dbCursor.execute(selectExt2IntMappingQuery, (topic, ))
                r = dbCursor.fetchall()
                
                if len(r) == 1:
                    topicTo = r[0].topic_to
                    internalClient.publish(topicTo, payload)
                    CACHE_OF_MESSAGE.add(getMessageHash(topicTo, payload))
                    print('E: {}={} -> {}={}'.format(topic, payload, topicTo, payload))
                else:
                    print('E: {}={} -> X'.format(topic, payload))
                    
        EXTERNAL_CACHE = []

    if len(INTERNAL_CACHE):
        for row in INTERNAL_CACHE:
            topic, payload = row
            hash = getMessageHash(topic, payload)
            
            if hash in CACHE_OF_MESSAGE:
                CACHE_OF_MESSAGE.remove(hash)
            else:
                dbCursor.execute(selectInt2ExtMappingQuery, (topic, ))
                r = dbCursor.fetchall()
                
                if len(r) == 1:
                    topicTo = r[0].topic_to
                    externalClient.publish(topicTo, payload)
                    CACHE_OF_MESSAGE.add(getMessageHash(topicTo, payload))
                    print('I: {}={} -> {}={}'.format(topic, payload, topicTo, payload))
                else:
                    print('I: {}={} -> X'.format(topic, payload))
        
        INTERNAL_CACHE = []
        
    externalClient.loop(0.00001)
    internalClient.loop(0.00001)

dbCursor.close()
dbConn.close()