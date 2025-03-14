from abc import ABC, abstractmethod

#from DomotiPi.DeviceAbstract import DeviceAbstract


class IsDeviceServiceInterface(ABC):
    """
    IsDeviceServiceInterface
    "Interface" for Device Services

    :extends:   ABC
    """
    @abstractmethod
    def factory(self, device: object):
        pass

    @abstractmethod
    def connect(self):
        pass