"""
DomotiPi development testscript

Abstract Light device test script
Device: DomotiPi.Device.Light
"""

from DomotiPi.Device.Light.Light import Light


# DomotiPi.Device.Light test
light1 = Light()
print(light1.getName())
print(light1.getId())
print(light1.getDescription())
print(type(Light))

# objDump = dir(light1)
# print(objDump)
# print('----')
#
# pprint(objDump)