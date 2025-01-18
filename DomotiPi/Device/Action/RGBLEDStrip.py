import os
from operator import truediv

from gpiozero import RGBLED
from gpiozero.pins.pigpio import PiGPIOFactory
from os import environ

from DomotiPi.Device.Light import Light


class RGBLedStripMeta(type(Light), type(RGBLED)):
    pass


class RGBLEDStrip(Light, RGBLED, metaclass=RGBLedStripMeta):
    __pinRed: int
    __pinGreen: int
    __pinBlue: int

    def __init__(self):
        """
        Declare pin-numbers for red, green and blue

        NOTE: gpiozero uses GPIO pin-numbers instead of physical pin-numbers
        """
        self.__pinRed = 17  # Board 11
        self.__pinGreen = 22  # Board 13
        self.__pinBlue = 27  # Board 15

        """ Init parent classes RGBLED and Light """
        RGBLED.__init__(self, self.__pinRed, self.__pinGreen, self.__pinBlue)
        Light.__init__(self)

        """ Set PiGPIO address """
        os.environ["PIGPIO_ADDR"] = '192.168.20.25'
        pass

    def fu(self):
        pass
