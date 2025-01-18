import time

import os.path

import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish

import yaml

class Client():

    def __init__(self):
        self.mClient = mqttClient
        self.mPublish = mqttPublish

        brokerCfg: str = 'default_broker.yaml'
        if os.path.isfile('DomotiPi/mqtt/broker.yaml'):
            brokerCfg = 'broker.yaml'

        with open(f'DomotiPi/mqtt/{brokerCfg}') as configStream:
            self.config = yaml.safe_load(configStream)

        pass

    def listen(self):
        while True:
            self.mPublish.single(
                "homeassistant/domotipi/99/switch",
                payload="1",
                hostname=self.config['hostname'],
                port=self.config['port'],
                client_id=self.config['client_id'],
                auth={
                    'username':self.config['username'],
                    'password':self.config['password']
                },
                protocol=self.mClient.MQTTv311
            )

            time.sleep(4)



