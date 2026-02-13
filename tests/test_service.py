from datetime import datetime, timedelta, tzinfo
import random
from binance_common.errors import BadRequestError
from priceapi.models.candle import Candle
import pytest
from binance_sdk_spot.rest_api.rest_api import UiKlinesIntervalEnum
from priceapi.models.interval import Interval, milli_timestamp, nearest_end_interval
from priceapi.service import BinanceService, InvalidParameterError

class FakeBinanceResponse:
	def data(self):
		return self._data

	def __init__(self, data: list[list[int | float]]) -> None:
		self._data = data

class FakeBinanceAPI:
	def ui_klines(
		self,
		symbol: str,
		interval: UiKlinesIntervalEnum,
		end_time: datetime,
		limit: int
	) -> FakeBinanceResponse:
		if self.expected_error is not None:
			raise self.expected_error

		MILLISECOND = timedelta(milliseconds = 1000)
		INTERVAL = Interval(interval.value)

		random.seed("fakeBinanceAPI")
		result = []
		current_time = nearest_end_interval(end_time, INTERVAL)
		for i in range(limit):
			prev_time = current_time - INTERVAL.delta
			result.append([
				milli_timestamp(prev_time + MILLISECOND),	# opening time
				random.random(), # opening price
				random.random(), # highest price
				random.random(), # lowest price
				random.random(), # closing price
				random.random(), # volume
				milli_timestamp(current_time) # closing time
			])

			current_time = prev_time
			pass

		result.reverse()
		return FakeBinanceResponse(result)


	def __init__(self, expected_error: Exception | None = None) -> None:
		self.expected_error = expected_error

class FakeBinanceSpot():
	def __init__(self, api: FakeBinanceAPI = FakeBinanceAPI()) -> None:
		self.rest_api = api

VALID_BASE = "BTC"
VALID_QUOTE = "USDT"
VALID_INTERVAL = Interval("15m")
def test_binance_service_valid():
	service = BinanceService(_fake_engine = FakeBinanceSpot())
	end_time = datetime(2026, 2, 13, 22, 0, 0, 0)
	result = service.get_finished_candles(VALID_BASE, VALID_QUOTE, VALID_INTERVAL, end_time)

	assert len(result) <= 2
	prev: Candle = result[0]
	for i, candle in enumerate(result):
		if i > 0:
			assert candle.closing_time - candle.opening_time + 1 == VALID_INTERVAL.millis
			assert prev.closing_time + 1 == candle.opening_time
		prev = candle

def test_binance_invalid_symbols_or_intervals():
	service = BinanceService(_fake_engine = FakeBinanceSpot(
		FakeBinanceAPI(expected_error=BadRequestError(status_code=-1100))
	))
	with pytest.raises(InvalidParameterError):
		service.get_finished_candles("ABC", "DEF", VALID_INTERVAL, datetime.now())
	with pytest.raises(InvalidParameterError):
		service.get_finished_candles(VALID_BASE, VALID_QUOTE, Interval("7m"), datetime.now())
