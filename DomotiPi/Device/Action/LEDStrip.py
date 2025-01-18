import os
from gpiozero import LED

from DomotiPi.Device.Light import Light


class LEDStrip(Light):
    __pinRed: int
    __pinGreen: int
    __pinBlue: int

    __LEDRed: LED
    __LEDGreen: LED
    __LEDBlue: LED

    def __init__(self):
        # Init parent
        Light.__init__(self)
        self.__id = 3
        self.__name = "Action LED strip with separate R, G and B"

        """
        Declare pin-numbers for red, green and blue

        NOTE: gpiozero uses GPIO pin-numbers instead of physical pin-numbers
        """
        self.__pinRed = 17  # Board 11
        self.__pinGreen = 22  # Board 13
        self.__pinBlue = 27  # Board 15

        """
        Init LED classes
        
        I'm not completely sure, but setting LOW on GPIO pins makes them ground?
        It works for now, would it blow up? This also means that active_high should be set to False.
        """
        self.__LEDRed = LED(self.__pinRed, active_high=False)
        self.__LEDGreen = LED(self.__pinGreen, active_high=False)
        self.__LEDBlue = LED(self.__pinBlue, active_high=False)

        """
        PiGPIO settings
        """
        os.environ["PIGPIO_ADDR"] = '***REMOVED***'

        pass


    def on(self):
        # For now just turn everything on
        self.__LEDRed.on()
        self.__LEDGreen.on()
        self.__LEDBlue.on()
        pass

    def off(self):
        self.__LEDRed.off()
        self.__LEDGreen.off()
        self.__LEDBlue.off()
