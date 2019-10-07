# IoTGateway

Description
-----------

A smart kettle and a smart door connected to our IoT Gateway consisting of two MQTT brokers (i.e. Mosquitto)
and our forwarder script.

The first MQTT broker is an external broker.
Smart devices connected to it.
They use message topics like "DeviceID/field" that is useful for devices but not useful for automation scenarios.

The second one is an internal broker.
Automation scenarios and other subsystems connected to it.
They use message topics like "kitchen/kettle/status" or "kitchen/door/status".
For example,

        if kitchen.door.status == "opened" then
            kitchen.kettle.status = "on"

Our forwarder substitutes message topics from one format to another format when messages pass from external devices to internal subsystems and vice versa.
If your door or kettle breaks, you will buy new device (it will have another DeviceID) and just replace it and update topic mappings in our forwarder.

Installation
------------

    sudo apt-get update
    sudo apt-get install mosquitto mosquitto-clients
    sudo systemctl stop mosquitto
    sudo systemctl disable mosquitto


Quick start
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
