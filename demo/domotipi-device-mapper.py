"""
DomotiPi Device.Mapper demo/test script

"""
import demo_init
from DomotiPi.Device.Mapper import Mapper

demo_init.setPiGPIOEnv()

mapper = Mapper()
device = mapper.get(5)

print(f"type: {type(device)}")
print(device)
print(device.getHardwareVersion())
