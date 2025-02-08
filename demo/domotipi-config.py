"""
DomotiPi development testscript

Test / demo of DomotiPi.Config
"""
import demo_init

from DomotiPi.Config import Config


cfg = Config()
print(cfg)
print(cfg.getValue('pin_factory'))
print(cfg.getConfigStream())
