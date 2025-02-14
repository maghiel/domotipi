from gpiozero import RGBLED

from DomotiPi.Device.Light import Light


class RGBLEDStrip(Light):
    """
    Class LEDStrip. Extends Light.

    This class will talk to a dumb LED strip with separate r, g and b LEDs and creates different LED
    instances for each LED.
    Cheap strips like these are not suitable for usage with RGBLED, as colors can't be mixed.
\
    TODO: implement gpiozero.LED methods
    """
    __pinRed: int
    __pinGreen: int
    __pinBlue: int

    __RGBLED: RGBLED

    def __init__(self):
        """
        Constructor

        Sets parent, properties and instantiates LED objects for each pin
        """
        # Init parent
        Light.__init__(self)
        self._id = 4
        self._name = "Action RGB LED strip"
        self._description = "Action LED strip with RGB leds"

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
        self.__RGBLED = RGBLED(
            self.__pinRed,
            self.__pinGreen,
            self.__pinBlue,
            active_high=False,
            pwm=True
        )

        pass

    def on(self):
        """
        Switches all three LEDs on

        :rtype: bool
        """
        # For now just turn everything on
        self.__RGBLED.on()

        return True


    def off(self):
        """
        Switches all three LEDs off

        :rtype: bool
        """
        self.__RGBLED.off()

        return True


    def isLit(self):
        """
        Return state of the LED

        :return:
        """
        return self.__RGBLED.is_active


    def setColor(self, red: int or float, green: int or float, blue: int or float) -> bool:

        def convertColor(rgb: int or float):
            """
            convertColor
            Takes either int or float and converts the color to 0-1 format

            :param rgb:     Color value in either RGB 0-1 or 255
            :type rgb:      int or float
            :return:
            :rtype:         float
            """
            # If rgb is float assume rgb 0-1
            if type(rgb) == float:
                return rgb

            # Must already be rgb 0-1 if value is between 0 and 1
#            if 1 > rgb > 0:
#                return float(rgb)

            # Do not round the value!
            return float(rgb / 255)

        self.__RGBLED.red = convertColor(red)
        self.__RGBLED.green = convertColor(green)
        self.__RGBLED.blue = convertColor(blue)

        return True


    def setBrightness(self, brightness: int or float) -> bool:
        """
        Set brightness on red, green and blue

        :param brightness:  Brightness in 0-1 (float) or 0-255 (int) scale
        :type brightness:   int|float
        :return:
        :rtype:             bool
        """
        # Convert brightness to 0-1 scale if param is int
        if type(brightness) == int:
            brightness = brightness / 255

        self.__RGBLED.red.value = brightness
        self.__RGBLED.green.value = brightness
        self.__RGBLED.blue.value = brightness

        return True