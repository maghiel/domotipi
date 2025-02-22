"""
DomotiPi development testscript

Test / demo of the MQTT service for LEDStrip DomotiPi.Device.Hoogvliet.LEDStrip.Service.Mqtt
"""
import demo_init

from DomotiPi.Device.Hoogvliet.LEDStrip.Service.Mqtt import Mqtt

# Set the PiGPIO env
demo_init.setPiGPIOEnv()

try:
    stripCtl = Mqtt()
except KeyboardInterrupt:
    # TODO: close connection to mqtt broker
    demo_init.cleanUp()
