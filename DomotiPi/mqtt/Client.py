import time

import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish

from DomotiPi.Config import Config


class Client:
    """
    Class DomotiPi.mqtt.Client

    Simple MQTT client

    Instead of extending mqtt classes new instances are made.
    """

    config: dict

    mClient: mqttClient
    mPublish: mqttPublish

    def __init__(self):
        """
        Constructor. Instantiate MQTT client and publish objects and load configuration
        """
        self.mClient = mqttClient
        self.mPublish = mqttPublish

        cfg = Config()
        self.config = cfg.getValue('mqtt')
        # TODO: try throw catch

        pass

    def listen(self):
        def onMessage(self, userdata, message):
            print(f"Incoming message!: {message.payload}")

        client = self.mClient.Client()
        client.username_pw_set(
            self.config['client']['username'],
            self.config['client']['password']
        )
        client.connect(
            self.config['host']['hostname'],
            self.config['host']['port']
        )

        client.on_message = onMessage
        client.subscribe('homeassistant/domotipi/99/switch')

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