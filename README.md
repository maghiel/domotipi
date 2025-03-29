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

DomotiPi is currently not a package because I consider it way too alpha to be so.

DomotiPi is ment to be run on bare metal, but since it utilizes gpiozero it can also be ran from a control machine,
or even using a mockup device. Please review `config.yaml` for instructions how to do so.

## Download

### Using git
The most flexible of downloading DomotiPi is using git, as it allows you to switch branches easily. No configuration
will be lost if you use `config.yaml` instead of the default template as no other information is stored locally 
(subject to change).

#### HTTPS
```bash
git clone https://github.com/maghiel/domotipi.git
```

#### SSH
Prerequisites having a GitHub account configured.
```bash
git@github.com:maghiel/domotipi.git
```

### Downloading a tarball or zip
Alternatively just download the latest release.

```bash
mkdir domotipi
cd domotipi
wget https://github.com/maghiel/domotipi/archive/refs/tags/v0.1.0.0-prealpha.4.tar.gz
tar -zxvf v0.1.0.0-prealpha.4.tar.gz
```

## Setup
First of all a virtual environment has to be created, preferably using Python 3.13 or above.

Debian users will need to install `python-venv` first if not installed! Python will warn you about that.

```bash
# Create the venv
python -m venv .venv
# Activate the venv
source .venv/bin/activate
```

### Upgrade PIP
To be sure, let's first upgrade PIP in our fresh venv:
```bash
python -m pip install --upgrade pip
```

### Installing requirements
This will install the basic requirements, without any packages needed for communication with the device.
```bash
pip install -r requirements.txt
```

#### Requirements for local device control
When you intend to control the device directly from the computer it is attached to, the following will suffice:
```bash
pin install -r requirements-local.txt
```

#### Requirements for remote device control
Remote control requires `pigpio`, which can be installed in the venv by running:

```bash
pip install -r requirements-remote.txt
```

## Run
To check if all is well, simply try:
```bash
python main.py
```

# Configuration
A template for configuration is stored in `config-default.yaml`. You can directly modify `config-default.yaml` but it
is recommended to copy it to `default.yaml`. DomotiPi will load `config.yaml` if found, and fall back to the default 
in case it's missing.

Configuration options are explained in the configuration file. 

# Usage
The preferred method of setting up a device is through configuration. Please review the default configuration to learn 
how to do so.

## Through config

An example can be found in `demo/domoti-device-mapper.py`

## Using arguments

An example can be found in `demo/domotipi-device-light-led-rgbled.py`

