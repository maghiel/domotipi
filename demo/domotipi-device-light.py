"""
DomotiPi development testscript

Abstract Light device test script
Device: DomotiPi.Device.Light
"""
import demo_init
from DomotiPi.Device.Light import Light


# DomotiPi.Device.Light test
light1 = Light()
print(light1.getName())
print(light1.getId())
print(type(Light))