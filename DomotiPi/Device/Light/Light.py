from DomotiPi.DeviceAbstract import DeviceAbstract


class Light(DeviceAbstract):
    """
    Class Light, Extends abstract :class:`DeviceAbstract`
    Base class for light emitting devices (see what I did there?)
    """

    _id: int
    _name: str
    _description: str

    def __init__(self):
        """
        Constructor
        """
        self._id = 1
        self._name = "Light"
        self._description = "Base Light class"

    def getId(self) -> int:
        """
        Get ID of Device

        :rtype: int
        :return:
        """
        return self._id

    def getName(self) -> str:
        """
        Return name of Device

        :return:
        :rtype: str
        """
        return self._name

    def getDescription(self) -> str:
        """
        Return description of Device

        :return:
        :rtype: str
        """
        return self._description