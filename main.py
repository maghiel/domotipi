# DomotiPi example main.py script
from DomotiPi.Device.Mapper import Mapper

# Instantiate mapper and retrieve device 6 from config
mapper = Mapper()
device = mapper.get(6)

# Try to connect the device to the service
try:
    device.getService().connect()
except KeyboardInterrupt:
    device.off()
    device.getService().getClient().disconnect()
    print("Exit by user.")
