# This is a sample Python script.
import os
from time import sleep

from DomotiPi.Device.Light import Light

#from DomotiPi.Device.Action.RGBLEDStrip import RGBLEDStrip

from DomotiPi.Device.Action.LEDStrip import LEDStrip

from DomotiPi.Config import Config

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

cfg = Config()
print(cfg)
print(cfg.getConfigStream())


'''os.environ["GPIOZERO_PIN_FACTORY"] = 'pigpio'
os.environ["PIGPIO_ADDR"] = '***REMOVED***'

strip = LEDStrip()
strip.on()

sleep(10)

strip.off()'''


'''light1 = Light()
print(light1.getName())
print(light1.getId())
print(type(Light))


strip = RGBLEDStrip()
strip.getId()
'''


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

