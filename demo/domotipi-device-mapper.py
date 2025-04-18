"""
DomotiPi Device.Mapper demo/test script

"""

import demo_init
from DomotiPi.Device.Mapper import Mapper

demo_init.setPiGPIOEnv()


mapper = Mapper()
device = mapper.get(6)

try:
    device.getService().connect()
except KeyboardInterrupt:
    device.off()
    device.getService().getClient().disconnect()
    demo_init.cleanUp()
