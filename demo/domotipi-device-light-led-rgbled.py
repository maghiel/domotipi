"""
DomotiPi development testscript

Basic led strip on and off test
Device: DomotiPi.Device.Light.LED.RGBLED
"""

import demo_init
from time import sleep

from DomotiPi.Device.Light.LED.RGBLED import RGBLED


# Set the pigpio environment
demo_init.setPiGPIOEnv()

# DomotiPi.Device.Action.LED test
# Basic led strip on and off test
strip = RGBLED()
strip.on()

sleep(5)

strip.off()