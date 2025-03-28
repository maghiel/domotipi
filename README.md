# First of all
Please, I repeat, please(!) **do not** take this project too serious. Consider it my little sandbox hobby project, 
made in the little spare time I have to work on it.

Second, I am not a python developer. I am open to learning, but I refuse to adhere to snake_case everywhere. 

DomotiPi *does* work however and I intend to keep maintaining it actively.

Finally, yes. Ofcourse I am aware of existing solutions. Yes, I am aware of the fact that I'm reinventing the wheel for 
a large part.

# DomotiPi
>Overkill home automation with Raspberry Pi.

## Why?
Be cheap. Buy Tuya. Flash it. Run locally. @$#%@, firmware update. Flashing becomes a challenge, love it.
Sht, the integration broke. Don't have time for this anymore.<br/>

Why am I doing this? Wait.....I have tons of Pi's around. What if I just buy even cheaper dumb devices, just use GPIO. 
Well not that cheap, Pi is overkill, but well, I have them anyway! 

## What?
**DomotiPi** is a project to make your dumb hardware smart with the Pi's you have and hopefully integrate with your 
existing home automation.

Take a Pi, Home Assistant, a cheap LED strip and your soldering iron, create a config file or a new class, and done.

Instead of taking the eas path of creating an MQTT device through configuration in Home Assistant, 
I want my devices to be automatically discovered and ready to use. Thus, reinventing the wheel. 

# Installation

# Configuration
A template for configuration is stored in _config-default.yaml._ You can directly modify _config-default.yaml_ but it
is recommended to copy it to _default.yaml._ DomotiPi will load _config.yaml_ if found, and fall back to the default 
in case it's missing.

Configuration options are explained in the configuration file. 

# Usage
The preferred method of setting up a device is through configuration. Please review the default configuration to learn 
how to do so.

## Through config

An example can be found in `demo/domoti-device-mapper.py`

## Using arguments

An example can be found in `demo/domotipi-device-light-led-rgbled.py`

