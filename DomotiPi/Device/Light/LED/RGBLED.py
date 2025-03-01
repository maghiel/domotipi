from gpiozero import RGBLED as RGBLEDIO

from DomotiPi.Device.Light.Light import Light


class RGBLED(Light):
    """
    Class RGBLED. Extends Light.
    SoundLogic RGB LED Strip sold at Hoogvliet stores.

    This class will talk to a dumb RGB LED strip using gpiozero.RGBLED

    TODO: implement gpiozero.RGBLED methods
    """
    __pinRed: int
    __pinGreen: int
    __pinBlue: int

    __RGBLED: RGBLEDIO

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
        self.__RGBLED = RGBLEDIO(
            self.__pinRed,
            self.__pinGreen,
            self.__pinBlue,
            active_high=False,
            pwm=True
        )

        # Store current color values
        self.setColorValue(
            self.__RGBLED.red,        # Red
            self.__RGBLED.green,      # Green
            self.__RGBLED.blue,       # Blue
            1               # Brightness
        )

        pass


    def setColorValue(self, red : float, green : float, blue : float, brightness : float):
        """
        Sets property colorValue with r,g,b and brightness values in 0-1 scale.
        Typically used for "remembering" the last brightness setting in order to calculate proper factor.

        :param red:             Red
        :param green:           Green
        :param blue:            Blue
        :param brightness:      Brightness
        :raises:                ValueError
        """
        args = locals()
        for arg in args.items():
            if type(arg[1]) == type(self):
                continue

            if arg[1] < 0 or arg[1] > 1:
                raise ValueError('RGB values must be between 0 and 1')

        self._colorValue = [
            red,            # Red
            green,          # Green
            blue,           # Blue
            brightness      # Brightness
        ]


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


    def toggle(self):
        """
        Toggle on/off state on LEDs
        """
        self.__RGBLED.toggle()


    def isLit(self) -> bool:
        """
        Return state of the LED

        :return:
        :rtype:     bool
        """
        return self.__RGBLED.is_active


    def setColor(self, red: int or float, green: int or float, blue: int or float) -> bool:
        """
        Sets new color with given r,g and b values.
        Accepts both RGB 0-1 and 255.

        :param red:     Red LED value
        :type red:      int or float
        :param green:   Green LED value
        :type green:    int or float
        :param blue:    Blue LED value
        :type blue:     int or float
        :return:
        :rtype:         bool
        """
        def convertColor(rgb: int or float) -> float:
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

        red = convertColor(red)
        green = convertColor(green)
        blue = convertColor(blue)

        self.__RGBLED.red = red
        self.__RGBLED.green = green
        self.__RGBLED.blue = blue

        # Store color values and pretend brightness is 1
        self.setColorValue(
            red,
            green,
            blue,
            1
        )

        return True


    def setBrightness(self, brightness: int or float) -> bool:
        """
        Sets brightness equally on red, green and blue.
        Accepts both RGB 0-1 and 255 as arguments.

        :param brightness:  Brightness value in either RGB 0-1 or 255
        :type brightness:   int or float
        :return:
        :rtype:             bool
        """
        # Convert brightness to 0-1 scale if param is int
        if type(brightness) == int:
            brightness = brightness / 255

        # Calculate factor from current/previous brightness
        brightnessFactor = brightness / self._colorValue[3]

        def calcColor(color : float, factor : float) -> float:
            """
            Calculate new color value with given brightness factor.

            :param color:       Old color value
            :type color:        float
            :param factor:      Difference factor between old and new brightness
            :type factor:       float
            :return:
            :rtype:             float
            """
            color = color * factor
            if color > 1:
                color = 1
            elif color < 0:
                color = 0

            return color

        # Set new value on all LEDs
        self.__RGBLED.red = calcColor(self.__RGBLED.red, brightnessFactor)
        self.__RGBLED.green = calcColor(self.__RGBLED.green, brightnessFactor)
        self.__RGBLED.blue = calcColor(self.__RGBLED.blue, brightnessFactor)

        # Store new values
        self.setColorValue(
            self.__RGBLED.red,
            self.__RGBLED.green,
            self.__RGBLED.blue,
            brightness
        )

        return True


    def blink(self):
        """
        Blink all LEDs with current color as on_color
        """
        self.__RGBLED.blink(on_color=self.__RGBLED.color)


    def pulse(self):
        """
        Pulse all LEDs with current color as on_color
        """
        self.__RGBLED.pulse(on_color=self.__RGBLED.color)
