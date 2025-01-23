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

    def getConfigStream(self) -> dict:
        """
        Attempt to open stream to YAML and return dictionary.
        Method will attempt
            - cfgFile
            - cfgDefaultFile

        :rtype: dict
        :return:
        """
        cfgIO = self.cfgDefaultFile
        if os.path.isfile(self.cfgFile):
            cfgIO = self.cfgFile
        elif not os.path.isfile(self.cfgDefaultFile):
            # TODO: throw exception
            print('error')

        with open(f'{cfgIO}') as ioStream:
            configStream = yaml.safe_load(ioStream)

        return configStream

    def getValue(self, index: str) -> any:
        """
        Get value for given index

        :param index:

        :return:
        :rtype: any
        """
        if not index in self.cfg.keys():
            print(f'error, key {index} not found')
            # TODO: Throw exception
            return

        return self.cfg.get(index)
