from DomotiPi.Device.Hoogvliet.LEDStrip.Hoogvliet import Hoogvliet
from DomotiPi.mqtt.Client import Client


class Mqtt(Hoogvliet):
    """
    Class DomotiPi.Device.Action.LEDStrip.Service.Mqtt

    Mqtt service layer for LEDStrip.

    TODO: Layer should be an injectable factory
    TODO: Save states on disconnect/remember states
    TODO: Extend base exception classes

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

        self.objectId = 'domotipi-hoogvliet_ledstrip' + str(self.getId())

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
                'brightness': False,
                'color': (
                    'r',
                    'g',
                    'b',
                ),
                'supported_color_modes': 'rgb',
                #'color_mode' : 'rgb',              # Deprecated!
                #'color_temp': 0,                   # probably not needed
        }

        self.client.configure(configTopic, payload)

        ledState = super().isLit()

        self.client.publishSingle(
            self.topic['state'],
            {
                'state': 'OFF' if ledState == False else 'ON',
                'brightness' : 255
            }
        )


    def command(self, state: dict):
        """
        Set given state/execute command
        This method is typically called by the mqtt client from a payload.
        Commands like "color" and "brightness" are automatically extracted from the payload.

        :param state:       State to change to
        :type state:        dict
        :return:
        :rtype:             bool
        :raises:            ValueError
        TODO: Refactor state to command
        """
        # state ON|OFF, switch LED on|off and publish single message to broker to report back
        if "state" in state.keys():
            match state.get('state'):
                case "ON":
                    if not super().isLit():
                        # Turn on LEDs and publish ON state
                        super().on()
                        self.client.publishSingle(
                            self.topic['state'],
                            {'state': 'ON'}
                        )
                case "OFF":
                    if super().isLit():
                        # Turn off LEDs and publish OFF state
                        super().off()
                        self.client.publishSingle(
                            self.topic['state'],
                         {'state': 'OFF'}
                        )
                case _:
                    super().off()
                    raise ValueError(f'State must be either ON or OFF, received {state.get('state')}')

        # Color state, call parent with given rgb-255
        if 'color' in state.keys():
            self.color(state.get('color'))

        # brightness state, call parent with given brightness-255
        if 'brightness' in state.keys():
            self.brightness(state.get('brightness'))

        return True


    # def state(self, payload):
    #     return True


    def getState(self) -> bool:
        """
        Return current state
        Return weather or not the device is on or off

        :return:
        :rtype: bool
        """
        return super().isLit()


    def brightness(self, payload: int):
        """
        Set brightness

        :param payload:     Brightness in 255 format
        :type payload:      int
        :return:
        :rtype:             bool
        :raises:            ValueError
        """
        if payload > 255 or payload < 0:
            raise ValueError(f'Brightness expected 0-255, {payload} received instead.')
        super().setBrightness(payload)

        return True


    def color(self, colorPayload: dict) -> bool:
        """
        Set color from payload with rgb
        Call parent setColor with given color values

        :param colorPayload:    Payload with {r,g,b}
        :type colorPayload:     dict
        :return:
        :rtype:                 bool
        :raises:                ValueError
        """
        if (
            not 'r' in colorPayload.keys()
            or not 'g' in colorPayload.keys()
            or not 'b' in colorPayload.keys()
        ):
            raise ValueError('Invalid colorPayload, should be {r,g,b}.')

        super().setColor(
            colorPayload.get('r'),
            colorPayload.get('g'),
            colorPayload.get('b')
        )

        return True
