"""
demo_init.py

Changes working dir to parent.
This script should be included by every demo script
"""

import os
import sys
from pathlib import Path


scriptPath = Path(os.path.dirname(__file__))    # Create Path instance for cwd (typically /root/demo)
os.chdir(scriptPath.parent)                     # Change wd to parent
sys.path.insert(0, str(scriptPath.parent) + "/")    # Append trailing slash for cross-platform compatibility

from DomotiPi.Config import Config


def setPiGPIOEnv():
    cfg = Config()
    pinFactory = cfg.getValue("pin_factory")

    os.environ["GPIOZERO_PIN_FACTORY"] = pinFactory

    if pinFactory == "pigpio":
        os.environ["PIGPIO_ADDR"] = cfg.getValue("pigpio_addr")


def cleanUp():
    print("DomotiPi gracefully exiting by User interrupt")
