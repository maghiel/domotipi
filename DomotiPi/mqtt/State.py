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

    def getState(self) -> str:
        """
        Return device state as string ON or OFF

        :return:
        :rtype: str
        """
        return self._state

    def setState(self, state: str):
        """
        Set device state.

        :param state:   Either ON or OFF
        :type state:    str
        """
        if state != "ON" and state != "OFF":
            raise DomotiPiError("state must be either ON or OFF")

        self._state = state

    def getBrightness(self) -> int:
        """
        Get brightness

        :return:
        :rtype: int
        """
        return self._brightness

    def setBrightness(self, brightness: int):
        """
        Set brightness

        :param brightness:
        :type brightness: int
        """
        self._brightness = brightness
        pass

    def getColor(self) -> dict:
        """
        Return color dict

        :return:
        :rtype: dict
        """
        return self._color

    def setColor(self, color: dict):
        """
        Set color dict.

        :param color:   Dict of r,g,b
        :type color:    dict
        :return:
        """
        self._color = color
        pass

    def getEffect(self) -> str:
        """
        Return effect

        :return:
        :rtype: str`
        """
        return self._effect

    def setEffect(self, effect: str | None):
        """
        Set effect

        :param effect:
        :type effect: str | None
        :return:
        """
        self._effect = effect
        pass

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