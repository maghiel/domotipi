import importlib

from DomotiPi.Config import Config
from DomotiPi.Device.Exception.DeviceNotFoundErrror import DeviceNotFoundError
from DomotiPi.Device.Abstract import Abstract


class Mapper:
    """
    Class DomotiPi.Device.Mapper

    Map Device from Config
    """

    _config: Config

    def __init__(self):
        """
        Constructor.
        Sets Config instance.

        """
        self._setConfig(Config())

        pass

    def _getConfig(self) -> Config:
        """
        Return Config instance.

        :return:
        :rtype: Config
        """
        return self._config

    def _setConfig(self, config: Config):
        """
        Set Config instance.

        :param config:
        :type config: Config
        :return:
        """
        self._config = config

    def get(self, deviceId: any) -> Abstract:
        """
        Get populated Device from Config by id

        :param deviceId:
        :type deviceId: any
        :raises: DeviceNotFoundError
        :return:
        :rtype: Abstract
        """
        device = self._getRaw(deviceId)

        if not device:
            raise DeviceNotFoundError(
                f"No device has been configured with id: {deviceId}"
            )

        return self._populate(device)

    def _getRaw(self, deviceId: any) -> dict | None:
        """
        Return device configuration by id.

        :param deviceId:    DeviceId, typically an integer. Pass 'default' to get default settings.
        :type deviceId:     any
        :return:
        :rtype:             dict | None
        """
        cfg = self._getConfig()
        devices = dict(cfg.getValue("devices"))

        device = devices.get(deviceId)

        return device

    def _getDefaultAttributes(self) -> dict:
        """
        Return dict with default device attributes

        :raises: DeviceNotFoundError
        :return:
        :rtype: dict
        """
        defaults = self._getRaw("default")

        if not defaults:
            raise DeviceNotFoundError("Default device configuration not found!")

        return defaults

    def _populate(self, deviceCfg: dict) -> Abstract:
        """
        Populate and instantiate Device with given dictionary.

        :param deviceCfg:
        :type deviceCfg: dict
        :return:
        :rtype: Abstract
        """
        deviceType = str(deviceCfg.get("type"))

        # Try to import the device by device_type set in config
        module = importlib.import_module(f"DomotiPi.Device.{deviceType}")
        class_ = deviceType.split(".")[-1]

        deviceClass = getattr(module, class_)

        # Fetch attributes from config and populate with default values for unset.
        param = deviceCfg
        defaults = self._getDefaultAttributes()
        for default in defaults.items():
            param.setdefault(default[0], default[1])

        # Magic on some attributes
        # Skip type, never an attribute
        if "type" in param:
            param.pop("type")
        # Set Service layer
        if "service" in param:
            if not param.get("service") or param.get("service") is None:
                param.pop("service")

            # Instantiate service class
            path = deviceType.split(".")

            serviceModule = importlib.import_module(
                f"DomotiPi.Device.{path[0]}.{path[1]}.Service.{param.get('service')}"
            )
            serviceClass_ = getattr(serviceModule, param.get("service"))

            param.update({"service": serviceClass_()})
        # Parse GPIO
        if "gpio" in param:
            # Replace gpio by its child properties
            for k, v in param["gpio"].items():
                param[k] = v

            param.pop("gpio")

        # CamelCase All Keys
        newParam = param.copy()
        for key in param:
            camelKey = self.__toCamel(key)
            if camelKey != key:
                newParam[camelKey] = param[key]
                newParam.pop(key)

        return deviceClass(**newParam)

    @staticmethod
    def __toCamel(word: str) -> str:
        """
        Convert python preferred lower_case to camelCase

        :param word:
        :type word: str
        :return:
        :rtype: str
        """
        if not word.find("_"):
            return word

        words = word.split("_")

        camel = ""
        i = 0

        for word in words:
            if i == 0:
                camel += word
                i += 1
                continue

            camel += word[0].upper() + word[1:]

        return camel
