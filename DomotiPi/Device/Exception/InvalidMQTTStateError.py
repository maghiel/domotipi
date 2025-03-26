from DomotiPi.Exception.DomotiPiError import DomotiPiError


class InvalidMQTTStateError(DomotiPiError):
    """
    InvalidMQTTStateError. Extends DomotiPiError.
    Raised when a received MQTT state message is unknown or invalid.

    """
    pass