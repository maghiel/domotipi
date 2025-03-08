from DomotiPi.Device.IsDeviceServiceInterface import IsDeviceServiceInterface
from DomotiPi.DeviceAbstract import DeviceAbstract


class Light(DeviceAbstract):
    """
    Class Light, Extends abstract :class:`DeviceAbstract`
    Base class for light emitting devices (see what I did there?)
    """

    def __init__(self, id: int, name: str, description: str, service: IsDeviceServiceInterface):
        """
        Constructor.
        Calls setOptions and sets arguments as properties

        :param id:              Device identifier
        :type id:               int
        :param name:            Device name
        :type name:             str
        :param description:     Device description
        :type description:      str
        :param service:         Device service (MQTT, REST, ...)
        :type service:          IsDeviceServiceInterface
        """
        options = locals()
        self.setOptions(options)


    def setOptions(self, options: dict):
        """
        Set class properties from given dict of arguments

        :param options:     Arguments passed to typically the constructor
        :type options:      Dict
        :return:
        :rtype:             self
        """
        for option in options.items():
            if type(option[1]) == type(self):
                continue

            # Generate method name from option key
            method = f"set{option[0][0].upper() + option[0][1:]}"

            # Call setter with value.
            # Non-callable methods are simply skipped to allow more freedom in extending classes
            if callable(setter := getattr(self, method, 'None')):
                setter(option[1])
                continue

        return self


    def getId(self) -> int:
        return super().getId()

    def setId(self, deviceId: int) -> int:
        return super().setId(deviceId)

    def getName(self) -> str:
        return super().getName()

    def setName(self, name: str) -> str:
        return super().setName(name)

    def getDescription(self) -> str:
        return super().getDescription()

    def setDescription(self, description: str) -> str:
        return super().setDescription(description)

    def getService(self) -> IsDeviceServiceInterface:
        return super().getService()

    def setService(self, service : IsDeviceServiceInterface):
        return super().setService(service)