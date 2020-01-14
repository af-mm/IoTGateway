FROM python:3.7

WORKDIR /IoTGateway

COPY config.py forwarder.py requirements.txt ./

RUN pip3 install -r requirements.txt

ENV EMQTT_BROKER_HOST=localhost \
	EMQTT_BROKER_PORT=1024 \
	EMQTT_LOGIN=gw \
	EMQTT_PSWD=b0b3e594420357e78eb8554aebc77231 \
	IMQTT_BROKER_HOST=localhost \
	IMQTT_BROKER_PORT=1025 \
	DB_HOST=localhost \
	DB_PORT=1026 \
	DB_USER=postgres \
	DB_PSWD=1234 \
	DB_NAME=IoTSystemDB \
	DB_E2I_MAPPING_TABLE=gw_e2i_mapping \
	DB_I2E_MAPPING_TABLE=gw_i2e_mapping

CMD [ "python3", "./forwarder.py" ]