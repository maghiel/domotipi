import importlib

from DomotiPi.Config import Config
from DomotiPi.Device.DeviceNotFoundErrror import DeviceNotFoundError
from DomotiPi.DeviceAbstract import DeviceAbstract


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

    def get(self, deviceId: any):
        """
        Get populated Device from Config by id

        :param deviceId:
        :type deviceId: any
        :return:
        :rtype: DeviceAbstract
        """
        cfg = self._getConfig()
        devices = dict(cfg.getValue('devices'))

        device = devices.get(deviceId)

        if not device:
            raise DeviceNotFoundError(f'No device has been configured with id: {deviceId}')

        return self._populate(device)

    def _populate(self, deviceCfg: dict) -> DeviceAbstract:
        """
        Populate and instantiate Device with given dictionary.

        :param deviceCfg:
        :type deviceCfg: dict
        :return:
        :rtype: DeviceAbstract
        """
        deviceType = str(deviceCfg.get('type'))

        # Try to import the device by device_type set in config
        module = importlib.import_module(f"DomotiPi.Device.{deviceType}")
        class_ = deviceType.split('.')[-1]

        deviceClass = getattr(module, class_)

        # Create list of attributes from config
        param = []
        for attr in deviceCfg.items():
            if attr[0] == "type":   # Skip type, never an attribute
                continue
            if attr[0] == "gpio":
                # Get pins list from gpio
                param.append(attr[1].get('pins'))
                continue
            if attr[0] == "service":
                # Instantiate service class
                path = deviceType.split('.')

                serviceModule = importlib.import_module(f"DomotiPi.Device.{path[0]}.{path[1]}.Service.{attr[1]}")
                serviceClass_ = getattr(serviceModule, attr[1])
                param.append(serviceClass_())
                continue

            param.append(attr[1])   # In all other cases append the attribute

        return deviceClass(*param)