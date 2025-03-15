from abc import ABC, abstractmethod


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
