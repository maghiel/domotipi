import demo_init
from DomotiPi.Device.Mapper import Mapper

demo_init.setPiGPIOEnv()

mapper = Mapper()
devices = mapper.get(5)

print('HELLO!')
print(f"type: {type(devices)}")
print(devices)
