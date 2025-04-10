from DomotiPi.Device.Exception.DeviceTypeError import DeviceTypeError
from DomotiPi.Device.Exception.InvalidMQTTStateError import InvalidMQTTStateError
from DomotiPi.Device.Exception.LightCommandError import LightCommandError
from DomotiPi.Device.Exception.LightValueError import LightValueError

from DomotiPi.Device.IsDeviceServiceInterface import IsDeviceServiceInterface
from DomotiPi.Device.Light.LED.RGBLED import RGBLED

from DomotiPi.mqtt.Client import Client
from DomotiPi.mqtt.State import State as MqttState

from DomotiPi.Config import Config


class Mqtt(IsDeviceServiceInterface):
    """
    Class DomotiPi.Device.Light.LED.Service.Mqtt

    Mqtt service layer for LED.

    client      DomotiPi.mqtt.Client    MQTT client
    mqttState   DomotiPi.mqtt.State     MQTT State instance
    device      DomotiPi.DeviceAbstract Device instance
    objectId    string                  Unique object ID based on name and ID of parent
    topic       dict                    Topic dictionary to be defined in constructor
    """

    NS_DEVICE = "domotipi"

    _client: Client
    _mqttState: MqttState
    _device: RGBLED

    objectId: str
    topic: dict
    _topicPrefix: str

    def __init__(self, topicPrefix=""):
        """
        Constructor
        Instantiate MQTT client and State instance and set topicPrefix.
        Additionally, factory should be called by the parent device.

        :param topicPrefix:
        :type topicPrefix:  str
        """
        self.setClient(Client())
        self._setMqttState(MqttState())

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

        # Define topics. Alternatively all topics could be based of home(~),
        # but for readability I'm leaving it like this
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

        :raises:    DeviceTypeError
        :return:
        """
        if not isinstance(self.getDevice(), RGBLED):
            raise DeviceTypeError(
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

    def _getMqttState(self) -> MqttState:
        """
        Get MQTT State instance

        :return:
        :rtype: DomotiPi.mqtt.State
        """
        return self._mqttState

    def _setMqttState(self, mqttState: MqttState):
        """
        Set MQTT State instance

        :param mqttState:
        :type mqttState: DomotiPi.mqtt.State
        :return:
        """
        self._mqttState = mqttState
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

        TODO: hardcoded device properties should be configurable
        TODO: differentiate device registry, origin, etc.

        :param topic:           Home/base topic to subscribe/announce too
        :type topic:            str
        :param configTopic:     Configuration/discovery topic
        :type configTopic:      str
        :return:                None
        """
        payload = {
            # Topics and settings
            "~": topic,
            "cmd_t": "~/set",
            "stat_t": "~/state",
            "schema": "json",
            # Device properties
            "manufacturer": self.getDevice().getManufacturer(),
            "model": self.getDevice().getModel(),
            "hw_version": self.getDevice().getHardwareVersion(),
            "sw_version": self.getDevice().getSoftwareVersion(),
            "support_url": self.getDevice().getSupportURL(),
            "suggested_area": self.getDevice().getSuggestedArea(),
            # Device settings
            "name": self.getDevice().getName(),
            "uniq_id": self.objectId,
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
            "retain": True,
            #'color_mode' : 'rgb',              # Deprecated!
            #'color_temp': 0,                   # probably not needed
        }

        self.getClient().configure(configTopic, payload)

        mqttState = self._getMqttState()
        mqttState.setState("OFF" if self.getDevice().isLit() == False else "ON")

        self.getClient().publishSingle(
            self.topic["state"],
            mqttState.getAsDict()
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
        :raises:            InvalidMQTTStateError
        """
        # state ON|OFF, switch LED on|off and publish single message to broker to report back
        if "state" in state.keys():
            match state.get("state"):
                case "ON":
                    if not self.getDevice().isLit():
                        # Turn on LEDs and publish ON state
                        self.getDevice().on()
                        # Call other Light properties in order to recover state before OFF
                        # but not after a disconnect as it would destroy the retained messages.
                        if self._getMqttState().getState() is not None:
                            self.commandLight(self._getMqttState().getAsDict())

                        self._getMqttState().setState("ON")
                case "OFF":
                    if self.getDevice().isLit():
                        # Turn off LEDs, set OFF state and clear all effects
                        self.getDevice().off()
                        self._getMqttState().setState("OFF")
                        self._getMqttState().setEffect(None)
                case _:
                    self.getDevice().off()
                    raise InvalidMQTTStateError(
                        f"State must be either ON or OFF, received {state.get('state')}"
                    )

        # Call commandLight for other states
        self.commandLight(state)

        # Publish the state back to the broker
        self.getClient().publishSingle(
            self.topic['state'],
            self._getMqttState().getAsDict(),
            True
        )

        return True

    def commandLight(self, state: dict):
        """
        Command Light with color, brightness or effect

        :param state:   Payload with possible effects
        :type state:    dict
        :return:
        """
        # Color state, call parent with given rgb-255
        if "color" in state.keys():
            self.color(state.get("color"))

        # brightness state, call parent with given brightness-255
        if "brightness" in state.keys():
            self.brightness(state.get("brightness"))

        # It's disco time
        if "effect" in state.keys():
            self.effect(state.get("effect"))

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
        :raises:            LightValueError
        """
        if payload > 255 or payload < 0:
            raise LightValueError(f"Brightness expected 0-255, {payload} received instead.")

        self.getDevice().setBrightness(payload)
        self._getMqttState().setBrightness(payload)

        return True

    def color(self, colorPayload: dict) -> bool:
        """
        Set color from payload with rgb
        Call parent setColor with given color values

        :param colorPayload:    Payload with {r,g,b}
        :type colorPayload:     dict
        :return:
        :rtype:                 bool
        :raises:                LightValueError
        """
        if (('r', 'g', 'b') - colorPayload.keys()).difference():
            raise LightValueError("Invalid colorPayload, should be {r,g,b}.")

        # Set colors on physical device
        self.getDevice().setColor(
            colorPayload.get("r"),
            colorPayload.get("g"),
            colorPayload.get("b")
        )

        # Set colors in the state instance
        self._getMqttState().setColor(colorPayload)

        return True

    def effect(self, effect: str) -> bool:
        """
        Call parent with given effect

        :param effect:  The effect to use
        :type effect:   str
        :return:
        :raises:        LightCommandError
        """
        match effect:
            case "normal":
                self.getDevice().toggle()
            case "blink":
                self.getDevice().blink()
            case "pulse":
                self.getDevice().pulse()
            case _:
                raise LightCommandError(f"Effect {effect} not supported by device.")

        self._getMqttState().setEffect(effect)

        return True
