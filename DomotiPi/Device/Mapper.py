import importlib

from DomotiPi.Config import Config
from DomotiPi.Device.DeviceNotFoundErrror import DeviceNotFoundError
from DomotiPi.DeviceAbstract import DeviceAbstract


class Mapper:
    _config: Config

    def __init__(self):
        self._setConfig(Config())

        pass

    def _getConfig(self) -> Config:
        return self._config

    def _setConfig(self, config: Config):
        self._config = config

    def get(self, deviceId: any):
        cfg = self._getConfig()
        devices = dict(cfg.getValue('devices'))

        device = devices.get(deviceId)

        if not device:
            raise DeviceNotFoundError(f'No device has been configured with id: {deviceId}')

        return self._populate(device)

    def _populate(self, deviceCfg: dict) -> DeviceAbstract:
        deviceType = str(deviceCfg.get('type'))

        module = importlib.import_module(f"DomotiPi.Device.{deviceType}")
        class_ = deviceType.split('.')[-1]

        deviceClass = getattr(module, class_)

        print(deviceClass)
        print(type(deviceClass))
        param = []
        for attr in deviceCfg.items():
            if attr[0] == "type":
                continue
            if attr[0] == "gpio":
                param.append(attr[1].get('pins'))
                continue
            if attr[0] == "service":
                path = deviceType.split('.')

                serviceModule = importlib.import_module(f"DomotiPi.Device.{path[0]}.{path[1]}.Service.{attr[1]}")
                serviceClass_ = getattr(serviceModule, attr[1])
                param.append(serviceClass_())
                continue

            param.append(attr[1])

        return deviceClass(*param)