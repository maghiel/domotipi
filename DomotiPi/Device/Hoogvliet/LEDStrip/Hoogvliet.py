from gpiozero import RGBLED

from DomotiPi.Device.Light import Light


class Hoogvliet(Light):
    """
    Class LEDStrip. Extends Light.

    This class will talk to a dumb LED strip with separate r, g and b LEDs and creates different LED
    instances for each LED.
    Cheap strips like these are not suitable for usage with RGBLED, as colors can't be mixed.

    TODO: implement gpiozero.LED methods
    """
    __pinRed: int
    __pinGreen: int
    __pinBlue: int

    __RGBLED: RGBLED

    _colorValue: list

    def __init__(self):
        """
        Constructor

        Sets parent, properties and instantiates LED objects for each pin
        """
        # Init parent
        Light.__init__(self)
        self._id = 5
        self._name = "Hoogvliet SoundLogic RGB LED strip"
        self._description = "Tuya RGB LED strip with SoundLogic brand sold at Hoogvliet in the bargain bin."

        """
        Declare pin-numbers for red, green and blue

        NOTE: gpiozero uses GPIO pin-numbers instead of physical pin-numbers
        """
        self.__pinRed = 17  # Board 11
        self.__pinGreen = 27  # Board 13
        self.__pinBlue = 22  # Board 15

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

        self._colorValue = [
            self.__RGBLED.red,      # Red
            self.__RGBLED.green,    # Green
            self.__RGBLED.blue,     # Blue
            1                       # Brightness
        ]

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

        # Store color values and pretend brightness is 1
        self.setColorValue(
            convertColor(red),
            convertColor(green),
            convertColor(blue),
            1
        )

        return True


    def setBrightness(self, brightness: int or float) -> bool:
        # Convert brightness to 0-1 scale if param is int
        if type(brightness) == int:
            brightness = brightness / 255

        # Calculate factor from current/previous brightness
        brightnessFactor = brightness / self._colorValue[3]

        def calcColor(color, factor):
            color = color * factor
            if color > 1:
                color = 1
            elif color < 0:
                color = 0

            return color
        # def calcFactor(ledValue, brightnessValue):
        #     return ledValue * brightnessValue / 255

        self.__RGBLED.red = calcColor(self.__RGBLED.red, brightnessFactor)
        self.__RGBLED.green = calcColor(self.__RGBLED.green, brightnessFactor)
        self.__RGBLED.blue = calcColor(self.__RGBLED.blue, brightnessFactor)

        self.setColorValue(
            self.__RGBLED.red,
            self.__RGBLED.green,
            self.__RGBLED.blue,
            brightness
        )

        return True

    def setColorValue(self, red : float, green : float, blue : float, brightness : float):
        self._colorValue = [
            red,            # Red
            green,          # Green
            blue,           # Blue
            brightness      # Brightness
        ]

    # def setBrightness(self, brightness: int or float) -> bool:
    #     """
    #     Set brightness on red, green and blue
    #
    #     :param brightness:  Brightness in 0-1 (float) or 0-255 (int) scale
    #     :type brightness:   int|float
    #     :return:
    #     :rtype:             bool
    #     """
    #     print(f"pre-brightness: {brightness}")
    #     # Convert brightness to 0-1 scale if param is int
    #     if type(brightness) == int:
    #         brightness = brightness / 255
    #     print(f"brightness after division: {brightness}")
    #
    #     def calcFactor(ledValue, brightnessValue):
    #         if ledValue > brightnessValue:
    #             return ledValue * brightnessValue
    #
    #         if brightnessValue > ledValue:
    #             return ledValue * (brightnessValue + 1)
    #
    #         # newValue = (ledValue * (brightnessValue / 1))
    #         # if newValue >= 1:
    #         #     newValue = newValue / 10
    #
    #         #newValue = ledValue * brightnessValue
    #         print(f'NEWVALUE: {newValue}')
    #         if newValue >= 1:
    #             return 1
    #         return newValue
    #
    #     print(f'brightness is: {brightness}')
    #
    #     print(f'red: {self.__RGBLED.red}')
    #     print(f"value will be set to {self.__RGBLED.red} * (1 / {brightness}")
    #     self.__RGBLED.red = calcFactor(self.__RGBLED.red, brightness)
    #     print(f'red after: {self.__RGBLED.red}')
    #     self.__RGBLED.green = calcFactor(self.__RGBLED.green, brightness)
    #     self.__RGBLED.blue = calcFactor(self.__RGBLED.blue, brightness)
    #
    #     return True