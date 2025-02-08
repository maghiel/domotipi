from DomotiPi.Device.Action.LEDStrip.LEDStrip import LEDStrip
from DomotiPi.mqtt.Client import Client


class Mqtt(LEDStrip):
    """
    Class DomotiPi.Device.Action.LEDStrip.Service.Mqtt

    Mqtt service layer for LEDStrip.

    TODO: Layer should be an injectable factory
    TODO: Implement brightness
    TODO: Implement colors
    TODO: publish initial device state

    client      DomotiPi.mqtt.Client    MQTT client
    objectId    string                  Unique object ID based on name and ID of parent
    topic       dict                    Topic dictionary to be defined in constructor
    """
    client: Client

    objectId: str
    topic: dict

    def __init__(self):
        """
        Constructor

        Call parent constructor
        Set ObjectId
        Define MQTT topics
        Configure MQTT for discovery and subscribe to command topic
        """
        super().__init__()

        self.client = Client()

        self.objectId = 'domotipi-action_ledstrip' + str(self.getId())

        # TODO: all topics can be based of ~
        self.topic = {
            # Base
            'home': f"homeassistant/light/{self.objectId}",
            # Configuration
            'discover': f"homeassistant/light/{self.objectId}/config",
            # Command / set topic
            'command': f"homeassistant/light/{self.objectId}/set",
            # State topic
            'state': f"homeassistant/light/{self.objectId}/state"
        }

        self.configure(self.topic['home'], self.topic['discover'])

        # Subscribe to command topic. State will be called once per state-change.
        self.client.listen(
            self.topic['command'],
            'command',
            self,
            True
        )

        pass


    def configure(self, topic: str, configTopic: str) -> None:
        """
        Configure MQTT client for discovery

        :param topic:           Home/base topic to subscribe/announce too
        :type topic:            str
        :param configTopic:     Configuration/discovery topic
        :type configTopic:      str
        :return:                None
        """
        payload = {
                '~': topic,
                'name': self.getName(),
                'uniq_id': self.objectId + '-test',     # TODO: remove test suffix from uniq_id
                'cmd_t': '~/set',
                'stat_t': '~/state',
                'schema': 'json',
                'brightness': False
        }

        self.client.configure(configTopic, payload)


    def command(self, state: dict):
        """
        Set given state.
        This method is typically called by the mqtt client from a payload

        :param state:       State to change to
        :type state:        dict
        :return:boolean
        """
        if "state" in state.keys():
            match state.get('state'):
                case "ON":
                    # Turn on LEDs and publish ON state
                    super().on()
                    self.client.publishSingle(
                        self.topic['state'],
                        {'state': 'ON'}
                    )
                case "OFF":
                    # Turn off LEDs and publish OFF state
                    super().off()
                    self.client.publishSingle(
                        self.topic['state'],
                     {'state': 'OFF'}
                    )
                case _:
                    # TODO: throw exception about empty command/state OR implement toggle instead
                    super().off()

        return True


    def state(self, payload):
        return True

    def getState(self):
        return super().isLit()