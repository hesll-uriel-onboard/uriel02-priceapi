from datetime import datetime
from priceapi.models.interval import Interval
from priceapi.service import BinanceService, ServiceInterface

VALID_BASE = "BTC"
VALID_QUOTE = "USDT"
VALID_INTERVAL = Interval("15m")
def test_binance_service_OK():
	service = BinanceService()
	end_time = datetime.now()
	result = service.get_finished_candles(VALID_BASE, VALID_QUOTE, VALID_INTERVAL, end_time)
	assert len(result) <= 2

def test_binance_invalid_symbols():
	service = BinanceService()
	try:
		service.get_finished_candles("ABC", "DEF", VALID_INTERVAL, datetime.now())
	except ServiceInterface.InvalidParameterError:
		assert True
	except Exception as e:
		print(type(e))
		assert False

def test_binance_invalid_interval():
	service = BinanceService()
	try:
		service.get_finished_candles(VALID_BASE, VALID_QUOTE, Interval("7m"), datetime.now())
	except ServiceInterface.InvalidParameterError:
		assert True
	except Exception as e:
		print(type(e))
		assert False
