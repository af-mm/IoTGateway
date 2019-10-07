# IoTGateway

INSTALLATION
------------

    sudo apt-get update
    sudo apt-get install mosquitto mosquitto-clients
    sudo systemctl stop mosquitto
    sudo systemctl disable mosquitto


QUICK START
-----------

To start IoTGateway, each line bellow should be started in different terminals:

    mosquitto -p 1024
    mosquitto -p 1025
    python3 door.py
    python3 kettle.py
    python3 forwarder.py
    python3 scenario.py
    
To imitate an event that the door has just been opened, you can use the following command:

    mosquitto_pub -h "localhost" -p 1024 -t "0000000001/state" -m "opened"
