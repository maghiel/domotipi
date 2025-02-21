"""
DomotiPi development testscript

Basic led strip on and off test
Device: DomotiPi.Device.Hoogvliet.LEDStrip.Hoogvliet
"""

import demo_init
from time import sleep

from DomotiPi.Device.Hoogvliet.LEDStrip.Hoogvliet import Hoogvliet

# Set the pigpio environment
demo_init.setPiGPIOEnv()

# DomotiPi.Device.Action.LEDStrip test
# Basic led strip on and off test
strip = Hoogvliet()
strip.on()

sleep(5)

strip.off()