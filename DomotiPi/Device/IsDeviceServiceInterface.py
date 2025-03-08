from abc import ABC, abstractmethod

class IsDeviceServiceInterface(ABC):
    """
    IsDeviceServiceInterface
    "Interface" for Device Services

    :extends:   ABC
    """
    @abstractmethod
    def connect(self):
        pass