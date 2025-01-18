from abc import ABC, abstractmethod


class DeviceAbstract(ABC):

    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass