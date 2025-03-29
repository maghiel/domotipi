# DomotiPi example main.py script
from DomotiPi.Device.Mapper import Mapper

mapper = Mapper()
device = mapper.get(6)

try:
    device.getService().connect()
except KeyboardInterrupt:
    device.off()
    device.getService().getClient().disconnect()
    print("Exit by user.")