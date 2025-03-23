from abc import ABC, abstractmethod

import DomotiPi.mqtt.Client


class IsDeviceServiceInterface(ABC):
    """
    IsDeviceServiceInterface
    "Interface" for Device Services

    :extends:   ABC
    """

    @abstractmethod
    def factory(self, device: object):
        # TODO: circular reference making strong typing impossible.
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def getClient(self) -> DomotiPi.mqtt.Client.Client:
        pass