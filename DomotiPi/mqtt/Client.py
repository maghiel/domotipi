from paho.mqtt.client import Client as mqttClient
from paho.mqtt.subscribeoptions import SubscribeOptions

import json

from DomotiPi.Config import Config


class Client:
    """
    Class DomotiPi.mqtt.Client
    Simple MQTT client utilizing Paho's.

    Instead of extending mqtt classes new instances are made.
    """
    _config: dict
    _client: mqttClient

    def __init__(self):
        """
        Constructor.

        Instantiate MQTT client and publish objects and load configuration
        """
        # Configuration
        cfg = Config()
        self.setConfig(cfg.getValue("mqtt"))

        # Instantiate and connect client
        try:
            self.setClient(self.connect())
        except Exception as e:
            e.add_note("Unable to connect to the MQTT broker.")
            raise

        pass

    def getConfig(self) -> dict:
        """
        Return configuration

        :return:
        :rtype: dict
        """
        return self._config

    def setConfig(self, config: dict) -> dict:
        """
        Set configuration

        :param config:
        :type config:   dict
        :return:
        :rtype:         dict
        """
        self._config = config
        return self.getConfig()

    def getClient(self) -> mqttClient:
        """
        Return paho MQTT client

        :return:
        :rtype: mqttClient
        """
        return self._client

    def setClient(self, client: mqttClient):
        """
        Set paho MQTT client

        :param client:
        :type client:   mqttClient
        :return:
        """
        self._client = client

    def connect(self) -> mqttClient:
        """
        Connect client to broker

        :return: mqttClient
        """
        client = mqttClient()
        client.username_pw_set(
            self.getConfig()["client"]["username"],
            self.getConfig()["client"]["password"],
        )
        client.connect(
            self.getConfig()["host"]["hostname"],
            self.getConfig()["host"]["port"],
        )

        return client

    def configure(self, topic: str, payload: dict, availTopic: str):
        """
        Configure mqtt discovery at given topic with given payload.
        Also set on_disconnect to allow updating the availability topic.

        :param topic:       Topic for discovery/configuration
        :type topic:        str
        :param payload:     Configuration payload
        :type payload:      dict
        :param availTopic:  Availability topic to publish to.
        :type availTopic:   str
        :return:            bool
        """
        def onDisconnect(client, userdata, rc):
            nonlocal availTopic
            self.publishSingle(availTopic, "offline")

        self.getClient().on_disconnect = onDisconnect

        self.getClient().publish(topic, json.dumps(payload))

        return True

    def listen(self, topic: dict, ctlType: str, ctlObject, loop: bool):
        """
        Listen/subscribe to given topic.

        Subscribe to given topic and optionally call object methods on on_message event.

        TODO: refactor to subscribe

        :param topic:       Topics to listen/subscribe too
        :type topic:        dict
        :param ctlType:     Control type; either "command" or "state"
        :type ctlType:      str
        :param ctlObject:   Object instance to call method on
        :type ctlObject:    TBD
        :param loop:        Call loop_forever on the MQTT client
        :type loop:         bool
        :return:
        """
        def onMessage(clientInstance: mqttClient, userdata, message):
            """
            MQTT hook on receiving message/payload

            :param clientInstance:  Not used, ctlObject calls our instance.
            :type clientInstance:   mqttClient
            :param userdata:        Not implemented yet.
            :param message:         Mqtt message
            :raises:                NotImplementedError
            """
            # Declare outer-scope variables
            nonlocal msgPrevious
            nonlocal getRetained
            nonlocal client

            # Decode mqtt payload to str and convert to dict
            msgdec = json.loads(message.payload.decode("utf-8"))

            # Unsubscribe from the state topic after a first success.
            # This will prevent continuous processing of a load of retained messages,
            # but will make sure the retained state is recovered after a disconnect.
            if msgPrevious is None:
                if msgdec:
                    msgPrevious = msgdec
                    getRetained = False
                    client.unsubscribe(topic["state"])
            elif msgdec == msgPrevious:
                client.unsubscribe(topic["state"])
                return

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

        msgPrevious = None
        getRetained = True

        client = self.getClient()
        client.on_message = onMessage

        # Only subscribe to the state topic to fetch retained messages after a disconnect or power off
        if getRetained:
            client.subscribe(topic["state"], options=SubscribeOptions(retainHandling=1))

        client.subscribe(topic["command"])

        if True == loop:
            client.loop_forever()

        pass

    def publishSingle(self, topic: str, message: dict | str, retain: bool = False):
        """
        Publish a single message to the MQTT broker.

        Typically used to publish state updates.

        TODO:   Investigate whether or not it's necessary to instantiate a new connection to the broker
                or the existing connection will suffice.

        :param topic:       Topic to publish message to
        :type topic:        str
        :param message:     Message to publish
        :type message:      dict | str
        :param retain:      Retain message. Defaults to false
        :type retain:       bool
        :return:
        """
        publisher = self.connect()
        publisher.loop_start()

        # Encode message in all cases besides a single string.
        # Not encoding single strings ensures properly sending availability payloads, where the payload
        # should be plain online/offline instead of being wrapped in quotes.
        # TODO: yes, I am aware this is a hack
        if not type(message) is str:
            message = json.dumps(message)

        publisher.publish(
            topic,
            payload=message,
            retain=retain
        )

        publisher.loop_stop()

    def loop(self):
        """
        Simply call loop_forever on the mqtt client.

        :return:
        """
        self.getClient().loop_forever()

    def disconnect(self):
        """
        Disconnect from the MQTT broker

        :return:
        """
        self.getClient().disconnect()
