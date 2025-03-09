import demo_init
from DomotiPi.Device.Light.LED.RGBLED import RGBLED

from DomotiPi.Device.Light.Light import Light
#from DomotiPi.Device.Light.LED import RGBLED
from DomotiPi.Device.Light.LED.Service import Mqtt
from DomotiPi import Config

cfg = Config

# light = Light(
#     123,
#     'test name',
#     'description of test device',
#     cfg
# )
#
# print(light.getId())
# print(light.getName())

light = RGBLED(
    5,
    'Hoogvliet',
    'Hoogvliet blabalba',
    Mqtt,
    {
        'red' : 17,
        'green' : 27,
        'blue' : 22
    }
)

light.getService().connect()



# light = RGBLED(
#     id,
#     name,
#     description,
#     service,
# )
# or
# light = RGBLED(
#     cfg.loadDevice(name)
# )
#
# light.setService(Mqtt)
#
# light.engage()
