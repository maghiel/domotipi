from DomotiPi.DeviceAbstract import DeviceAbstract


class Light(DeviceAbstract):
    """
    Class Light, Extends abstract :class:`DeviceAbstract`
    Base class for light emitting devices (see what I did there?)
    """

    def __init__(self, id: int, name: str, description: str, service: object):
        """
        Constructor
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

    def getService(self) -> object:
        return super().getService()

    def setService(self, service : object):
        return super().setService(service)