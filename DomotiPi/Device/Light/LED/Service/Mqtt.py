from DomotiPi.Device.IsDeviceServiceInterface import IsDeviceServiceInterface
from DomotiPi.Device.Light.LED.RGBLED import RGBLED
from DomotiPi.mqtt.Client import Client
from DomotiPi.Config import Config


class Mqtt(IsDeviceServiceInterface):
    """
    Class DomotiPi.Device.Light.LED.Service.Mqtt

    Mqtt service layer for LED.

    TODO: Save states on disconnect/remember states
    TODO: Extend base exception classes

    client      DomotiPi.mqtt.Client    MQTT client
    objectId    string                  Unique object ID based on name and ID of parent
    topic       dict                    Topic dictionary to be defined in constructor
    """

    NS_DEVICE = "domotipi"

    _client: Client
    _device: RGBLED

    objectId: str
    topic: dict
    _topicPrefix: str

    def __init__(self, topicPrefix=""):
        """
        Constructor
        Instantiate MQTT client and set topicPrefix.
        Additionally, factory should be called by the parent device.

        :param topicPrefix:
        :type topicPrefix:  str
        """
        self.setClient(Client())

        if not topicPrefix:
            cfg = Config().getValue("mqtt")
            topicPrefix = cfg["topic_prefix"]

        self.setTopicPrefix(topicPrefix)

        pass

    def factory(self, device: RGBLED):
        """
        'Manufacture' this service instance.
        Not a true factory, but well:
        Sets device instance,
        Sets MQTT topics

        :param device:  Device instance
        :type device:   RGBLED
        :return:
        :rtype:         self
        """
        self.setDevice(device)

        # Convert device name to "safe" name; lowercase and spaces replaced by underscores
        # TODO: remove special characters and move to a tool class
        deviceSafeName = (self.getDevice().getName()).lower().replace(" ", "_")

        # Set objectId from NS_DEVICE, safe name and id, by example: domotipi-mybrand_light-23
        self.objectId = (
            self.NS_DEVICE + "-" + deviceSafeName + "-" + str(device.getId())
        )

        prefix = f"{self.getTopicPrefix()}/light"

        # TODO: all topics can be based of ~
        self.topic = {
            # Base
            "home": f"{prefix}/{self.objectId}",
            # Configuration
            "discover": f"{prefix}/{self.objectId}/config",
            # Command / set topic
            "command": f"{prefix}/{self.objectId}/set",
            # State topic
            "state": f"{prefix}/{self.objectId}/state",
        }

        return self

    def connect(self):
        """
        Configure MQTT for discovery and subscribe to command topic

        :raises:    ReferenceError
        :return:
        """
        if not isinstance(self.getDevice(), RGBLED):
            raise ReferenceError(
                "Device not set. Was factory called before attempting to use the service?"
            )

        self.configure(self.topic["home"], self.topic["discover"])

        # Subscribe to command topic. State will be called once per state-change.
        self.getClient().listen(
            self.topic["command"],
            "command",
            self,
            True
        )


    def getClient(self) -> Client:
        """
        Return MQTT client

        :return:
        :rtype: DomotiPi.mqtt.Client
        """
        return self._client

    def setClient(self, client: Client):
        """
        Set the MQTT client.
        Note not just any client, like paho, can be used.

        :param client:
        :type client:   DomotiPi.mqtt.Client
        :return:
        :rtype:         self
        """
        self._client = client
        return self

    def getDevice(self) -> RGBLED:
        """
        Return LED device instance

        :return:
        :rtype: DomotiPi.Device.Light.LED.RGBLED
        """
        return self._device

    def setDevice(self, device: RGBLED):
        """
        Set the LED device instance

        :param device:
        :type device:   DomotiPi.Device.Light.LED.RGBLED
        :return:
        :rtype:         self
        """
        self._device = device
        return self

    def getTopicPrefix(self) -> str:
        """
        Return MQTT topic prefix

        :return:
        :rtype: str
        """
        return self._topicPrefix

    def setTopicPrefix(self, prefix: str):
        """
        Set MQTT topic prefix.
        Examples: home, living, homeassistant

        :param prefix:
        :type prefix:   str
        :return:
        """
        self._topicPrefix = prefix

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
            "~": topic,
            "name": self.getDevice().getName(),
            "uniq_id": self.objectId + "-test",  # TODO: remove test suffix from uniq_id
            "cmd_t": "~/set",
            "stat_t": "~/state",
            "schema": "json",
            "brightness": True,
            "color": (
                "r",
                "g",
                "b",
            ),
            "supported_color_modes": "rgb",
            "effect": True,
            "effect_list": (
                "normal",
                "blink",
                "pulse",
            ),
            #'color_mode' : 'rgb',              # Deprecated!
            #'color_temp': 0,                   # probably not needed
        }

        self.getClient().configure(configTopic, payload)

        ledState = self.getDevice().isLit()

        self.getClient().publishSingle(
            self.topic["state"],
            {
                "state": "OFF" if ledState == False else "ON",
                "brightness" : 255
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
            match state.get("state"):
                case "ON":
                    if not self.getDevice().isLit():
                        # Turn on LEDs and publish ON state
                        self.getDevice().on()
                        self.getClient().publishSingle(
                            self.topic["state"],
                            {"state": "ON"}
                        )
                case "OFF":
                    if self.getDevice().isLit():
                        # Turn off LEDs and publish OFF state
                        self.getDevice().off()
                        self.getClient().publishSingle(
                            self.topic['state'],
                            {"state": "OFF"}
                        )
                case _:
                    self.getDevice().off()
                    raise ValueError(
                        f"State must be either ON or OFF, received {state.get('state')}"
                    )

        # Color state, call parent with given rgb-255
        if "color" in state.keys():
            self.color(state.get("color"))

        # brightness state, call parent with given brightness-255
        if "brightness" in state.keys():
            self.brightness(state.get("brightness"))

        # It's disco time
        if "effect" in state.keys():
            self.effect(state.get("effect"))

        return True

    def getState(self) -> bool:
        """
        Return current state
        Return weather or not the device is on or off

        :return:
        :rtype: bool
        """
        return self.getDevice().isLit()

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
            raise ValueError(f"Brightness expected 0-255, {payload} received instead.")
        self.getDevice().setBrightness(payload)

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
            not "r" in colorPayload.keys()
            or not "g" in colorPayload.keys()
            or not "b" in colorPayload.keys()
        ):
            raise ValueError("Invalid colorPayload, should be {r,g,b}.")

        self.getDevice().setColor(
            colorPayload.get("r"),
            colorPayload.get("g"),
            colorPayload.get("b")
        )

        return True

    def effect(self, effect: str) -> bool:
        """
        Call parent with given effect

        :param effect:  The effect to use
        :type effect:   str
        :return:
        :raises:        ValueError
        """
        match effect:
            case "normal":
                self.getDevice().toggle()
            case "blink":
                self.getDevice().blink()
            case "pulse":
                self.getDevice().pulse()
            case _:
                raise ValueError(f"Effect {effect} not supported by device.")

        return True
