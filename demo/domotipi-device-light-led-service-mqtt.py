"""
DomotiPi development testscript

Test / demo of the MQTT service for LED DomotiPi.Device.Light.LED.Service.Mqtt
"""
import demo_init

from DomotiPi.Device.Light.LED.Service import Mqtt

# Set the PiGPIO env
demo_init.setPiGPIOEnv()

try:
    stripCtl = Mqtt()
except KeyboardInterrupt:
    # TODO: close connection to mqtt broker
    demo_init.cleanUp()
