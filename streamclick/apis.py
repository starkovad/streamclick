from oandapyV20 import API
from oandapyV20.endpoints.instruments import InstrumentsCandles
from oandapyV20.endpoints.accounts import AccountInstruments

from abc import ABCMeta, abstractmethod, abstractproperty
from configparser import ConfigParser

from datetime import datetime
from operator import itemgetter

class Api:
    def __init__(self, broker):
        _access_token, _account_id = self._acc_info(broker_name='Oanda')

        broker.connect(access_token=_access_token, account_id=_account_id)
        self._broker = broker
    
    def _acc_info(self, broker_name):
        config = ConfigParser()
        config.read('streamclick/.ini')

        broker_info = config[broker_name]
        return broker_info['access_token'], broker_info['account_id']

    def available(self, type_info=['name', 'type']):
        return self._broker.available(type_info=type_info)

    def iter_price(self,
                since,
                to=None,
                instrument='EUR_USD',
                ohlc='o',
                granularity='D',
                volume=False,
                abm='A'):
        '''
        Parse data with instrument candles.

        Args:
            since: the start of the time range to fetch candlesticks for.
            to: the end of the time range to fetch candlesticks for.
            ohlc: list of types(open, high, low, close) prices
            abm: ask, bid, mid
        Returns:
            generator object with datetime and open ask daily price by default.
        '''

        return self._broker.iter_price(since, to, instrument, ohlc, granularity, volume, abm)

class Broker(metaclass=ABCMeta):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def iter_price(self):
        pass

class Oanda(Broker):
    def connect(self, access_token, account_id):
        self.client = API(access_token=access_token)
        self.account_id = account_id

    def available(self, type_info):
        endpoint = AccountInstruments(accountID=self.account_id)
        rows = self.client.request(endpoint)

        for row in rows['instruments']:
            yield itemgetter(*type_info)(row) 
    
    def iter_price(self, since, to, instrument, ohlc, granularity, volume, abm):

        dt_format = '%Y-%m-%d %H:%M:%S'
        rfc3339 = '%Y-%m-%dT%H:%M:%S.%f000Z'

        iso_since = datetime.strptime(since, dt_format).isoformat()
        iso_to = None
        
        if to:
            iso_to = datetime.strptime(to, dt_format).isoformat()

        params = {
            'from': iso_since,
            'to': iso_to,
            'granularity': granularity,
            'price': abm
            }
        
        components = {
                'A': 'ask',
                'B': 'bid',
                'M': 'mid'
                }

        entrypoint = InstrumentsCandles(instrument=instrument, params=params)
        rows = self.client.request(entrypoint)
        instrument = rows['instrument']

        for row in rows['candles']:
            dt = datetime.strptime(row['time'], rfc3339)

            abm_values = row[components[abm]]
            price = itemgetter(*ohlc)(abm_values)

            if volume:
                yield dt, price, row['volume']
            else:
                yield dt, instrument, float(price)
