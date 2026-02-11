from datetime import datetime
from time import sleep
from priceapi.models.interval import Interval
from priceapi.service import BinanceService, ServiceInterface, milli_timestamp

def test_binance_service_OK():
	service = BinanceService()
	end_time = datetime.now()
	result = service.get_finished_candles("BTC", "USDT", Interval("15m"), end_time)
	assert len(result) <= 2

def test_binance_invalid_symbols():
	service = BinanceService()
	try:
		service.get_finished_candles("ABC", "DEF", Interval("15m"), datetime.now())
	except ServiceInterface.InvalidParameterError:
		assert True
	except Exception as e:
		print(type(e))
		assert False

def test_binance_invalid_interval():
	service = BinanceService()
	try:
		service.get_finished_candles("BTC", "USDT", Interval("7m"), datetime.now())
	except ServiceInterface.InvalidParameterError:
		assert True
	except Exception as e:
		print(type(e))
		assert False
