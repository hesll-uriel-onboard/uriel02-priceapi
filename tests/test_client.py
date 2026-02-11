from datetime import datetime
from priceapi.client import Client, ClientProvider
from priceapi.service import ServiceInterface, milli_timestamp

VALID_SYMBOLS = "BTC_USDT"
VALID_INTERVAL = "15m"
def test_OK():
	end_time = datetime.now()
	for provider in ClientProvider:
		client = Client()
		result = client.get_finished_candles(VALID_SYMBOLS, VALID_INTERVAL, end_time, provider = provider)
		for candle in result:
			assert candle.time_closed <= milli_timestamp(end_time)

def test_wrong_symbols():
	for provider in ClientProvider:
		client = Client()
		try:
			client.get_finished_candles("ABD-E?GH", VALID_INTERVAL, datetime.now(), provider = provider)
		except ServiceInterface.InvalidParameterError:
			pass
		except Exception:
			assert False

def test_wrong_interval():
	for provider in ClientProvider:
		client = Client()
		try:
			client.get_finished_candles(VALID_SYMBOLS, "7m", datetime.now(), provider = provider)
		except ServiceInterface.InvalidParameterError:
			pass
		except Exception:
			assert False
