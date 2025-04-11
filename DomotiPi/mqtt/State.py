from DomotiPi.Exception.DomotiPiError import DomotiPiError


class State:
    """
    Class State.
    Instance holding MQTT state properties during session.
    This class should clearly be abstracted and extended ;)

    TODO: Quick&dirty
    """
    _state: str = None
    _brightness: int = None
    _color: dict = None
    _effect: str = None

    def __init__(self):
        pass

    def getState(self):
        return self._state

    def setState(self, state: str):
        if state != "ON" and state != "OFF":
            raise DomotiPiError("state must be either ON or OFF")

        self._state = state

    def getBrightness(self) -> int:
        return self._brightness

    def setBrightness(self, brightness: int):
        self._brightness = brightness

    def getColor(self) -> dict:
        return self._color

    def setColor(self, color: dict):
        self._color = color

    def getEffect(self) -> str:
        return self._effect

    def setEffect(self, effect: str | None):
        self._effect = effect

    def getAsDict(self) -> dict:
        """
        Return State properties as a dict.
        Can be used as a message to publish to the broker.

        :return:
        :rtype: dict
        """
        state = dict()
        if self.getState() is not None:
            state["state"] = self.getState()
        if self.getBrightness() is not None:
            state["brightness"] = self.getBrightness()
        if self.getColor() is not None:
            state["color"] = self.getColor()
        if self.getEffect() is not None:
            state["effect"] = self.getEffect()

        return state