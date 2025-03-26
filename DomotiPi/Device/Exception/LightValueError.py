from DomotiPi.Exception.DomotiPiError import DomotiPiError


class LightValueError(DomotiPiError):
    """
    LightValueError. Extends DomotiPiError.
    Raised when trying to set an invalid value for a Light Device.
    For example when trying to set brightness higher than max.
    
    """
    pass