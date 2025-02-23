import os.path

import yaml


class Config:
    """
    Class Config

    Handles DomotiPi-wide configuration through YAML loading
    """
    cfgFile: str = "config.yaml"
    cfgDefaultFile: str = "config-default.yaml"

    cfg: dict

    def __init__(self):
        """
        Constructor, attempt loading config dictionary in self.cfg
        """
        self.cfg = self.getConfigStream()

        pass

    def getConfig(self) -> dict:
        """
        Get complete config dictionary

        :return:
        """
        return self.cfg

    def getConfigStream(self) -> dict:
        """
        Attempt to open stream to YAML and return dictionary.
        Method will attempt
            - cfgFile
            - cfgDefaultFile

        :rtype: dict
        :return:
        :raises:    FileNotFoundError
        """
        cfgIO = self.cfgDefaultFile
        if os.path.isfile(self.cfgFile):
            cfgIO = self.cfgFile
        elif not os.path.isfile(self.cfgDefaultFile):
            raise FileNotFoundError('Both default and custom configuration files not found.')

        with open(f'{cfgIO}') as ioStream:
            configStream = yaml.safe_load(ioStream)

        return configStream


    def getValue(self, index: str) -> any:
        """
        Get value for given index

        :param index:
        :type index:    str
        :return:
        :rtype:         any
        :raises:    IndexError
        """
        if not index in self.cfg.keys():
            raise IndexError(f'Key {index} not found.')

        return self.cfg.get(index)
