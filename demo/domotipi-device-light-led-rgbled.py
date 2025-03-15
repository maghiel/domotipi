"""
DomotiPi Device LED development/demo script


"""

import demo_init

from DomotiPi.Device.Light.LED.RGBLED import RGBLED
from DomotiPi.Device.Light.LED.Service.Mqtt import Mqtt


demo_init.setPiGPIOEnv()

service = Mqtt()

light = RGBLED(
    5,
    "Hoogvliet Abstraction",
    "Hoogvliet Abstraction Test",
    service,
    {
        "red" : 17,
        "green" : 27,
        "blue" : 22
    }
)

try:
    light.getService().connect()
except KeyboardInterrupt:
    light.off()
    demo_init.cleanUp()
