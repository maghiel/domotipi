import time

import os.path

import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish

import yaml

class Client:
    """
    Class DomotiPi.mqtt.Client

    Simple MQTT client

    Instead of extending mqtt classes new instances are made.
    """

    mClient: mqttClient
    mPublish: mqttPublish

    def __init__(self):
        """
        Constructor. Instantiate MQTT client and publish objects and load configuration from
        either default_broker.yaml or broker.yaml
        """
        self.mClient = mqttClient
        self.mPublish = mqttPublish

        brokerCfg: str = 'default_broker.yaml'
        if os.path.isfile('DomotiPi/mqtt/broker.yaml'):
            brokerCfg = 'broker.yaml'
        # TODO: throw exception when no config is found/default config is missing.

        with open(f'DomotiPi/mqtt/{brokerCfg}') as configStream:
            self.config = yaml.safe_load(configStream)

        pass

    def publish(self):
        """
        Publish simple payload to the MQTT broker

        :rtype: null
        """

        # Publish a simple payload every 4 seconds
        while True:
            self.mPublish.single(
                "homeassistant/domotipi/99/switch",
                payload= "1",
                hostname= self.config['hostname'],
                port= self.config['port'],
                client_id= self.config['client_id'],
                auth= {
                    'username': self.config['username'],
                    'password': self.config['password']
                },
                protocol= self.mClient.MQTTv311
            )

            time.sleep(4)