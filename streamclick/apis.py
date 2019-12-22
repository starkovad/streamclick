from oandapyV20 import API
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser

class Api:
    def __init__(self, broker):
        self._access_token = self._acc_info(broker_name='Oanda')
        self._broker = broker
    
    def _acc_info(self, broker_name):
        config = ConfigParser()
        config.read('streamclick/.ini')
        return config[broker_name]['access_token']

    def connect(self):
        return self._broker.connect(access_token=self._access_token)

class Broker(metaclass=ABCMeta):
    @abstractmethod
    def connect(self):
        pass

class Oanda(Broker):
    def connect(self, access_token):
        return access_token
