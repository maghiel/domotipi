"""
demo_init.py

Changes working dir to parent.
This script should be included by every demo script
"""
import os
from pathlib import Path

from DomotiPi.Config import Config

scriptPath = Path(os.path.dirname(__file__))    # Create Path instance for cwd (typically /root/demo)
os.chdir(scriptPath.parent)                     # Change wd to parent

def setPiGPIOEnv():
    cfg = Config()
    os.environ["GPIOZERO_PIN_FACTORY"] = cfg.getValue('pin_factory')
    os.environ["PIGPIO_ADDR"] = cfg.getValue('pigpio_addr')

def cleanUp():
    print("DomotiPi gracefully exiting by User interrupt")
