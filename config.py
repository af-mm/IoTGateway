import os

CFG = {
    'EXT_MQTT_BROKER': {
        'host': os.getenv('EMQTT_BROKER_HOST', 'localhost'),
        'port': int(os.getenv('EMQTT_BROKER_PORT', 20002)),
        'login': os.getenv('EMQTT_LOGIN', 'gw'),
        'password': os.getenv('EMQTT_PSWD', 'b0b3e594420357e78eb8554aebc77231')
    },
    'INT_MQTT_BROKER': {
        'host': os.getenv('IMQTT_BROKER_HOST', 'localhost'),
        'port': int(os.getenv('IMQTT_BROKER_PORT', 20021))
    },
    'db': {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 20004)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PSWD', '1234'),
        'dbname': os.getenv('DB_NAME', 'IoTSystemDB'),
        'table_e2i_mapping': os.getenv('DB_E2I_MAPPING_TABLE', 'gw_e2i_mapping'),
        'table_i2e_mapping': os.getenv('DB_I2E_MAPPING_TABLE', 'gw_i2e_mapping'),
    }
}

print(CFG)
