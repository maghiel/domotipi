from abc import ABC, abstractmethod

import validators

from DomotiPi.Device.IsDeviceServiceInterface import IsDeviceServiceInterface


class Abstract(ABC):
    """
    Abstract class Abstract. Extends abc.ABC
    Note: it goes against my nature to have implementations in abstract layers, but I guess that is what
    Python likes.
    """

    _id: int
    _name: str
    _description: str

    _manufacturer: str
    _model: str
    _hardwareVersion: str
    _softwareVersion: str
    _supportURL: str
    _suggestedArea : str

    _service: IsDeviceServiceInterface | None

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
    def getManufacturer(self) -> str:
        """
        Return Manufacturer name

        :return:
        :rtype str:
        """
        return self._manufacturer

    @abstractmethod
    def setManufacturer(self, manufacturer: str) -> str:
        """
        Set manufacturer name

        :param manufacturer:
        :type manufacturer: str
        :return:
        :rtype: str
        """
        self._manufacturer = manufacturer
        return self.getManufacturer()

    @abstractmethod
    def getModel(self) -> str:
        """
        Return model name

        :return:
        :rtype str:
        """
        return self._model

    @abstractmethod
    def setModel(self, model: str) -> str:
        """
        Set model name

        :param model:
        :type model: str
        :return:
        :rtype: str
        """
        self._model = model
        return self.getModel()

    @abstractmethod
    def getHardwareVersion(self) -> str:
        """
        Return hardware version

        :return:
        :rtype: str
        """
        return self._hardwareVersion

    @abstractmethod
    def setHardwareVersion(self, version: str) -> str:
        """
        Set hardware version

        :param version:
        :type version: str
        :return:
        :rtype: str
        """
        self._hardwareVersion = version
        return self.getHardwareVersion()

    @abstractmethod
    def getSoftwareVersion(self) -> str:
        """
        Return software version

        :return:
        :rtype: str
        """
        return self._softwareVersion

    @abstractmethod
    def setSoftwareVersion(self, version: str) -> str:
        """
        Set software version

        :param version:
        :type version: str
        :return:
        :rtype: str
        """
        self._softwareVersion = version
        return self.getSoftwareVersion()

    @abstractmethod
    def getSupportURL(self) -> str:
        """
        Return the support URL for the device.

        :return:
        :rtype: str
        """
        return self._supportURL

    @abstractmethod
    def setSupportURL(self, url: str):
        """
        Set the support URL for the device

        :param url:
        :type url: str
        :raises: ValueError
        :return:
        :rtype: str
        """
        if url != "" and not validators.url(url):
            raise ValueError(f'Invalid URL: {url}')

        self._supportURL = url
        return self.getSupportURL()

    @abstractmethod
    def getSuggestedArea(self) -> str:
        """
        Return suggested area for the device.

        :return:
        :rtype: str
        """
        return self._suggestedArea

    @abstractmethod
    def setSuggestedArea(self, area: str) -> str:
        """
        Set suggested area for the device.
        For example: home, living room, kitchen.

        :param area:
        :type area: str
        :return:
        :rtype: str
        """
        self._suggestedArea = area
        return self.getSuggestedArea()

    @abstractmethod
    def getService(self) -> IsDeviceServiceInterface | None:
        """
        Return device service-layer (for example MQTT, REST, etc.)

        TODO: abstraction layer for device services

        :return:
        :rtype: IsDeviceServiceInterface | None
        """
        return self._service

    @abstractmethod
    def setService(
        self, service: IsDeviceServiceInterface | None
    ) -> IsDeviceServiceInterface | None:
        """
        Set device service-layer.
        For example MQTT, REST, etc.

        :param service:
        :type service:  IsDeviceServiceInterface | None
        :return:
        :rtype:         IsDeviceServiceInterface | None
        """
        if service is None:
            self._service = None
            return self.getService()

        service.factory(self)

        self._service = service

        return self.getService()
