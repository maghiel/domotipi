# DomotiPi development testscript

import DomotiPi.Device.Action.LEDStrip

#from DomotiPi.Device.Action.RGBLEDStrip import RGBLEDStrip

#from DomotiPi.Device.Action.LEDStrip import LEDStrip
#from DomotiPi.Device.Action.LEDStrip.Service import Mqtt
from DomotiPi.Device.Action.LEDStrip.Service.Mqtt import Mqtt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
# DomotiPi.Config tests
cfg = Config()
print(cfg)
print(cfg.getValue('pin_factory'))
#print(cfg.getConfigStream())
'''

'''
# Environment setup
os.environ["GPIOZERO_PIN_FACTORY"] = cfg.getValue('pin_factory')
os.environ["PIGPIO_ADDR"] = cfg.getValue('pigpio_addr')
'''


'''
# MQTT test
mqtt = Client()
#mqtt.publish('woef woef woef')
#mqtt.listen()
mqtt.discovery()
'''

# LEDStrip / MQTT test
stripCtl = Mqtt()

'''
# DomotiPi.Device.Action.LEDStrip test
# Basic led strip on and off test

strip = LEDStrip()
strip.on()

sleep(10)

strip.off()
'''

'''
# DomotiPi.Device.Light test

light1 = Light()
print(light1.getName())
print(light1.getId())
print(type(Light))


strip = RGBLEDStrip()
strip.getId()
'''