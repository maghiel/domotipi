from DomotiPi.DeviceAbstract import DeviceAbstract


class Light(DeviceAbstract):
    """
    Class Light, Extends abstract :class:`DeviceAbstract`
    """

    __id: int
    __name: str

    def __init__(self):
        """
        Constructor
        """
        self.__id = 1
        self.__name = "Light"

    def getId(self) -> int:
        """
        Get ID of Device

        :rtype: int
        :return:
        """
        return self.__id

    def getName(self) -> str:
        """
        Return name of Device

        :rtype: str
        """
        return self.__name
