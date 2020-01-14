FROM python:3.7

WORKDIR /IoTGateway

COPY config.py .
COPY forwarder.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV EMQTT_BROKER_HOST localhost
ENV EMQTT_BROKER_PORT 1024
ENV EMQTT_LOGIN gw
ENV EMQTT_PSWD b0b3e594420357e78eb8554aebc77231
ENV IMQTT_BROKER_HOST localhost
ENV IMQTT_BROKER_PORT 1025
ENV DB_HOST localhost
ENV DB_PORT 1026
ENV DB_USER postgres
ENV DB_PSWD 1234
ENV DB_NAME IoTSystemDB
ENV DB_E2I_MAPPING_TABLE gw_e2i_mapping
ENV DB_I2E_MAPPING_TABLE gw_i2e_mapping

CMD [ "python3", "./forwarder.py" ]
