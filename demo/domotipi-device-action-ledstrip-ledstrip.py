"""
DomotiPi development testscript

Basic led strip on and off test
Device: DomotiPi.Device.Action.LEDStrip
"""

import demo_init
from time import sleep

from DomotiPi.Device.Action.LEDStrip.LEDStrip import LEDStrip

# Set the pigpio environment
demo_init.setPiGPIOEnv()

# DomotiPi.Device.Action.LEDStrip test
# Basic led strip on and off test
strip = LEDStrip()
strip.on()

sleep(5)

strip.off()