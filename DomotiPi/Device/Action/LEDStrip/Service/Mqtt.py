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
        print(self.getName())

        print(f"configured {self.objectId} ")
        print(self.topic)
        self.client.listen(self.topic['command'])
        #self.client.listen(self.topic['state'])

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
