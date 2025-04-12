import os
from DomotiPi.Config import Config


cfg = Config()
pinFactory = cfg.getValue("pin_factory")

os.environ["GPIOZERO_PIN_FACTORY"] = pinFactory

match pinFactory:
    case "lgpio":
        pass
    case "pigpio":
        os.environ["PIGPIO_ADDR"] = cfg.getValue("pigpio_addr")
    case _:
        pass
