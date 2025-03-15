# DomotiPi development testscript

import os
from DomotiPi.Config import Config

# from DomotiPi.Device.Action.RGBLEDStrip import RGBLEDStrip

# Load configuration
cfg = Config()

# Environment setup
os.environ["GPIOZERO_PIN_FACTORY"] = cfg.getValue("pin_factory")
os.environ["PIGPIO_ADDR"] = cfg.getValue("pigpio_addr")

"""
strip = RGBLEDStrip()
strip.getId()
"""
