from DomotiPi.Device.IsDeviceServiceInterface import IsDeviceServiceInterface
from DomotiPi.DeviceAbstract import DeviceAbstract


class Light(DeviceAbstract):
    """
    Class Light, Extends abstract :class:`DeviceAbstract`
    Base class for light emitting devices (see what I did there?)
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        service: IsDeviceServiceInterface = None,
        *args,
        **kargs,
    ):
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
        :type service:          IsDeviceServiceInterface or None
        """
        options = locals()
        self.setOptions(options)

    def setOptions(self, options: dict):
        """
        Set class properties from given dict of arguments.
        Non-callable methods are skipped to allow more freedom in extending classes.

        :param options:     Arguments passed to typically the constructor
        :type options:      Dict
        :return:
        :rtype:             self
        """
        for option in options.items():
            if type(option[1]) == type(self):
                continue

            # Call self if option is key-value pair. Potentially infinite :)
            if option[0] == "args":
                self.setOptions(options["args"][1])
                continue

            # Generate method name from option key
            method = f"set{option[0][0].upper() + option[0][1:]}"

            # Call setter with value.
            # Non-callable methods are simply skipped to allow more freedom in extending classes
            if callable(setter := getattr(self, method, "None")):
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

    def getManufacturer(self) -> str:
        return super().getManufacturer()

    def setManufacturer(self, manufacturer: str) -> str:
        return super().setManufacturer(manufacturer)

    def getModel(self) -> str:
        return super().getModel()

    def setModel(self, model: str) -> str:
        return super().setModel(model)

    def getHardwareVersion(self) -> str:
        return super().getHardwareVersion()

    def setHardwareVersion(self, version: str) -> str:
        return super().setHardwareVersion(version)

    def getSoftwareVersion(self) -> str:
        return super().getSoftwareVersion()

    def setSoftwareVersion(self, version: str) -> str:
        return super().setSoftwareVersion(version)

    def getSupportURL(self) -> str:
        return super().getSupportURL()

    def setSupportURL(self, url: str):
        return super().setSupportURL(url)

    def getSuggestedArea(self) -> str:
        return super().getSuggestedArea()

    def setSuggestedArea(self, area: str) -> str:
        return super().setSuggestedArea(area)

    def getService(self) -> IsDeviceServiceInterface:
        return super().getService()

    def setService(self, service: IsDeviceServiceInterface):
        return super().setService(service)
