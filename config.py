
CFG = {
    'EXT_MQTT_BROKER': {
        'host': 'iotfox.ru',
        'port': 20002
    },
    'INT_MQTT_BROKER': {
        'host': 'localhost',
        'port': 1025
    },
    'db': {
        'host': 'iotfox.ru',
        'port': 20004,
        'user': 'postgres',
        'password': '1234',
        'dbname': 'IoTSystemDB',
        'table_e2i_mapping': 'device.gw_e2i_mapping',
        'table_i2e_mapping': 'device.gw_i2e_mapping',
    }
}
