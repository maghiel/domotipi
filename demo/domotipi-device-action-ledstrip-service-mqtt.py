"""
DomotiPi development testscript

Test / demo of the MQTT service for LEDStrip DomotiPi.Device.Action.LEDStrip.Service.Mqtt
"""
import demo_init

from DomotiPi.Device.Action.LEDStrip.Service.Mqtt import Mqtt

# Set the PiGPIO env
demo_init.setPiGPIOEnv()

stripCtl = Mqtt()