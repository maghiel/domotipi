from os import MFD_ALLOW_SEALING

from DomotiPi.Device.Action.LEDStrip.LEDStrip import LEDStrip
from DomotiPi.mqtt.Client import Client


class Mqtt(LEDStrip):
    client: Client

    objectId: str
    topic: dict

    def __init__(self):
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

        # Subscribe to command topic
        self.client.listen(self.topic['state'], 'state', self, False)
        self.client.listen(self.topic['command'], 'command', self, False)

        self.client.loop()
        pass


    def configure(self, topic: str, configTopic: str):
        payload = {
                '~': topic,
                'name': self.getName(),
                'uniq_id': self.objectId + '-test',
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

        :param state: dict    State to change to
        :return:boolean
        """
        if "state" in state.keys():
            match state.get('state'):
                case "ON":
                    super().on()
                    self.client.publishSingle(
                        self.topic['state'],
                        {'state': 'ON'}
                    )
                case "OFF":
                    super().off()
                    # self.client.publishSingle(
                    #     self.topic['state'],
                    #  {'state': 'OFF'}
                    # )
                case _:
                    # TODO: throw exception about empty command/state OR implement toggle instead
                    super().off()

        return True

    def state(self, payload):
        return True

    def getState(self):
        return super().isLit()

