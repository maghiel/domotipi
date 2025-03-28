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
    "MyDevice",
    "MyDevice Test",
    service,
    {"red": 17, "green": 27, "blue": 22},
)

try:
    light.getService().connect()
except KeyboardInterrupt:
    light.off()
    light.getService().getClient().disconnect()
    demo_init.cleanUp()
