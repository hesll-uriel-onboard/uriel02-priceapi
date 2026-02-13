from datetime import datetime
from enum import Enum
from typing import override
from priceapi.client import Client, ClientProvider
from priceapi.service import BinanceService, milli_timestamp

from tests.test_service import FakeBinanceSpot

VALID_SYMBOLS = "BTC_USDT"
VALID_INTERVAL = "15m"

def build_fake():
	return BinanceService(_fake_engine = FakeBinanceSpot())

class Fake:
	@property
	def value(self):
		return self._value
	
	def __init__(self, value) -> None:
		self._value = value 
		pass
FAKE = Fake(value = build_fake)

def test_OK():
	end_time = datetime.now()
	for provider in ClientProvider:
		client = Client()
		result = client.get_finished_candles(VALID_SYMBOLS, VALID_INTERVAL, end_time, provider = FAKE)
		for candle in result:
			assert candle.closing_time <= milli_timestamp(end_time)
