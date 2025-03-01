from abc import ABC, abstractmethod


class DeviceAbstract(ABC):
    """
    Abstract class DeviceAbstract. Extends abc.ABC
    Note: it goes against my nature to have implementations in abstract layers, but I guess that is what
    Python likes.
    """

    _id: int
    _name: str
    _description: str

    _service: object


    @abstractmethod
    def getId(self) -> int:
        """
        Get Device id

        :return:
        :rtype: int
        """
        return self._id


    @abstractmethod
    def setId(self, deviceId: int) -> int:
        """
        Set Device id

        :param deviceId:    Device identifier
        :type deviceId:     int
        :return:
        :rtype:             int
        """
        self._id = deviceId
        
        return self.getId()


    @abstractmethod
    def getName(self) -> str:
        """
        Return Device name

        :return:
        :rtype: str
        """
        return self._name


    @abstractmethod
    def setName(self, name: str) -> str:
        """
        Set Device name

        :param name:    Device name
        :type name:     str
        :return:
        :rtype:         str
        """
        self._name = name

        return self.getName()


    @abstractmethod
    def getDescription(self) -> str:
        """
        Return Device description

        :return:
        :rtype: str
        """
        return self._description


    @abstractmethod
    def setDescription(self, description: str) -> str:
        """
        Set Device description

        :param description:     Description of the device
        :type description:      str
        :return:
        :rtype:                 str
        """
        self._description = description

        return self.getDescription()


    @abstractmethod
    def getService(self) -> object:
        """
        Return device service-layer (for example MQTT, REST, etc.)

        TODO: abstraction layer for device services
        TODO: stricter type casting

        :return:
        :rtype: object
        """
        return self._service


    @abstractmethod
    def setService(self, service: object) -> object:
        """
        Set device service-layer.
        For example MQTT, REST, etc.

        :param service:
        :type service:  object
        :return:
        :rtype:         object
        """
        self._service = service

        return self.getService()