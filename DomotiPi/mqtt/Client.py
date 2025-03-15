import paho.mqtt.client

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

    client: paho.mqtt.client.Client

    def __init__(self):
        """
        Constructor.

        Instantiate MQTT client and publish objects and load configuration
        """
        # Configuration
        cfg = Config()
        self.config = cfg.getValue("mqtt")

        # TODO: try throw catch

        # Instantiate and connect client
        self.client = self.connect()

        pass

    def connect(self) -> paho.mqtt.client.Client:
        """
        Connect client to broker

        :return: paho.mqtt.client.Client
        """
        client = paho.mqtt.client.Client()
        client.username_pw_set(
            self.config["client"]["username"],
            self.config["client"]["password"]
        )
        client.connect(
            self.config["host"]["hostname"],
            self.config["host"]["port"]
        )

        return client

    def configure(self, topic: str, payload: dict):
        """
        Configure mqtt discovery at given topic with given payload

        :param topic:       Topic for discovery/configuration
        :type topic:        str
        :param payload:     Configuration payload
        :type payload:      dict
        :return:            bool
        """
        self.client.publish(topic, json.dumps(payload))

        return True

    def listen(self, topic: str, ctlType: str, ctlObject, loop: bool):
        """
        Listen/subscribe to given topic.

        Subscribe to given topic and optionally call object methods on on_message event.

        TODO: refactor to subscribe

        :param topic:       Topic to listen/subscribe too
        :type topic:        str
        :param ctlType:     Control type; either "command" or "state"
        :type ctlType:      str
        :param ctlObject:   Object instance to call method on
        :type ctlObject:    TBD
        :param loop:        Call loop_forever on the MQTT client
        :type loop:         bool
        :return:
        """

        def onMessage(self, userdata, message):
            """
            MQTT hook on receiving message/payload

            :param message:
            :raises:        NotImplementedError
            """
            # Decode mqtt payload to str and convert to dict
            msgdec = json.loads(message.payload.decode("utf-8"))

            match ctlType:
                # Forward payload to ctlObject.command()
                case "command":
                    ctlObject.command(msgdec)
                # Forward state to ctlObject. Will probably be removed
                case "state":
                    ctlObject.state(msgdec)
                case _:
                    raise NotImplementedError(
                        "State topics other than command and state not implemented yet."
                    )

        client = self.client

        client.on_message = onMessage
        client.subscribe(topic)

        if True == loop:
            client.loop_forever()

        pass

    def publishSingle(self, topic: str, message: dict):
        """
        Publish a single message to the MQTT broker.

        Typically used to publish state updates.

        TODO:   Investigate whether or not it's necessary to instantiate a new connection to the broker
                or the existing connection will suffice.
        TODO:   Remove reference old code

        :param topic:       Topic to publish message to
        :type topic:        str
        :param message:     Message to publish
        :type message:      dict
        :return:
        """
        publisher = self.connect()
        publisher.loop_start()

        publisher.publish(
            topic,
            payload= json.dumps(message)
        )

        publisher.loop_stop()

        # Keeping the old stuff below for reference

        # self.client.loop_start()
        #
        # self.client.publish(
        #     topic,
        #     payload= json.dumps(message)
        # )
        #
        # self.client.loop_stop()

        # self.mPublish.single(
        #     topic,
        #     payload= json.dumps(message),
        #     hostname= self.config['host']['hostname'],
        #     port= self.config['host']['port'],
        #     client_id= self.config['client']['client_id'],
        #     auth= {
        #         'username': self.config['client']['username'],
        #         'password': self.config['client']['password']
        #     },
        #     protocol= self.mClient.MQTTv311
        # )

    def loop(self):
        """
        Simply call loop_forever on the mqtt broker.

        :return:
        """
        self.client.loop_forever()

    def disconnect(self):
        """
        Disconnect from the MQTT broker

        :return:
        """
        self.client.disconnect()
