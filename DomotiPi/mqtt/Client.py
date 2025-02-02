import time

import paho.mqtt.client
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish

import json

from DomotiPi.Config import Config


class Client:
    """
    Class DomotiPi.mqtt.Client

    Simple MQTT client

    Instead of extending mqtt classes new instances are made.

    TODO: lot of rename refactoring; client is used way too much
    TODO: remove testing methods
    """

    config: dict

    mClient: mqttClient
    mPublish: mqttPublish

    client: paho.mqtt.client.Client

    def __init__(self):
        """
        Constructor. Instantiate MQTT client and publish objects and load configuration
        """
        self.mClient = mqttClient
        self.mPublish = mqttPublish

        # Configuration
        cfg = Config()
        self.config = cfg.getValue('mqtt')

        # TODO: try throw catch

        # Instantiate and connect client
        self.client = self.connect()

        pass


    def connect(self) -> mqttClient.Client:
        """
        Connect client to broker

        :return: paho.mqtt.client.Client
        """
        client = self.mClient.Client()
        client.username_pw_set(
            self.config['client']['username'],
            self.config['client']['password']
        )
        client.connect(
            self.config['host']['hostname'],
            self.config['host']['port']
        )

        return client

    def configure(self, topic: str, payload: dict):
        print(topic)
        print(payload)
        self.client.publish(topic, json.dumps(payload))

        return True


    def discovery(self):
        topic = 'homeassistant/light/dopi-light-test01/config'
        payload = {
                '~': 'homeassistant/light/dopi-light_test01',
                'name': 'DomotiPi Light Test 01',
                'uniq_id': 'dopi-light_test01',
                'cmd_t': '~/set',
                'stat_t': '~/state',
                'schema': 'json',
                'brightness': False
            }
        client = self.client

        client.publish(topic, json.dumps(payload))
        time.sleep(1)
        client.loop_forever()


    def listen(self, topic):
        def onMessage(self, userdata, message):
            print(f"Incoming message!: {message.payload}")

        client = self.client

        client.on_message = onMessage
        client.subscribe(topic)
        print(f'subscribed to {topic}')

        client.loop_forever()


    def publish(self, payload: str):
        """
        Publish simple payload to the MQTT broker

        :type payload: str
        :rtype: null
        """

        # Publish a simple payload every 4 seconds
        while True:
            self.mPublish.single(
                "homeassistant/domotipi/99/switch",
                payload= payload,
                hostname= self.config['host']['hostname'],
                port= self.config['host']['port'],
                client_id= self.config['client']['client_id'],
                auth= {
                    'username': self.config['client']['username'],
                    'password': self.config['client']['password']
                },
                protocol= self.mClient.MQTTv311
            )

            time.sleep(4)