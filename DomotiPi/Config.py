import os.path

import yaml


class Config:
    configFile: str = "config.yaml"
    configDefaultFile: str = "config-default.yaml"

    config: yaml

    def __init__(self):
        self.getConfigStream()

        pass

    def getConfigStream(self):
        configIO = self.configDefaultFile
        if os.path.isfile(self.configFile):
            configIO = self.configFile
        elif not os.path.isfile(self.configDefaultFile):
            # TODO: throw exception
            print('error')

        with open(f'{configIO}') as ioStream:
            configStream = yaml.safe_load(ioStream)

        return configStream
