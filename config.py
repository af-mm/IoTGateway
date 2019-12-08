
CFG = {
    'EXT_MQTT_BROKER': {
        'host': 'localhost',
	'port': 20002
    },
    'INT_MQTT_BROKER': {
        'host': 'localhost',
        'port': 20021
    },
    'db': {
        'host': 'stepanov-backend.dev.local',
        'port': 20004,
        'user': 'postgres',
        'password': '1234',
        'dbname': 'IoTSystemDB',
        'table_e2i_mapping': 'device.gw_e2i_mapping',
        'table_i2e_mapping': 'device.gw_i2e_mapping',
    }
}
