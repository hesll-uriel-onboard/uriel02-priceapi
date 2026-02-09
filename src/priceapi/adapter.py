from abc import ABC, abstractmethod
from datetime import datetime
from typing import override

from binance_sdk_spot.rest_api.rest_api import UiKlinesIntervalEnum

from .models.candle import Candle
from binance_sdk_spot import Spot

def milli_timestamp(time: datetime) -> int:
	"""Convert the datetime to a POSIX timestamp, to the milliseconds.

	Example:
		```
		result = milli_timestamp(datetime.now())
		```
	"""
	return int(time.timestamp() * 1000)
def to_datetime(millis: int) -> datetime:
	"""Convert the millis timestamp to a datetime instance.

	Example:
		```
		result = to_datetime(1770635337208)
		# datetime.datetime(2026, 2, 9, 18, 8, 57, 208000)
		```
	"""
	return datetime.fromtimestamp(millis / 1000.0)

class ServiceInterface(ABC):
	"""An abstract interface of functionalities, that adapts for every market exchange.

	Example:
		```python
		market: ServiceInterface = BinanceService()
		result = market.get_finished_candles("BTCUSDT", "1m", datetime.now(), 2)
		```
	"""
	QUOTE = "USDT"
	class InvalidResponse(Exception):
		pass

	@abstractmethod
	def get_finished_candles(self,
		ticker_base: str,
		interval: str,
		end_time: datetime,
		limit: int = 2
	) -> list[Candle]:
		"""Return the last `limit` **finished** candles

		Example:
		```
		result = engine.get_finished_candles(end_time = datetime.now())
		```

		TODO:
			Implement this function in the adapters
		"""
		raise NotImplementedError

class BinanceService(ServiceInterface):
	"""Implementation of ServiceInterface for Binance"""

	class IntervalNotFoundError(Exception):
		"""Interval string is not one of the provided interval in Binance"""
		pass
	TIME_OPENED: int = 0
	PRICE_OPENED: int = 1
	PRICE_HIGH: int = 2
	PRICE_LOW: int = 3
	PRICE_CLOSED: int = 4
	VOLUME: int = 5
	TIME_CLOSED: int = 6

	def __init__(self) -> None:
		super().__init__()
		self.engine = Spot()

	@override
	def get_finished_candles(self,
		ticker_base: str,
		interval: str,
		end_time: datetime = datetime.now(),
		limit: int = 2
	) -> list[Candle]:
		"""See base class."""
		result = self.engine.rest_api.ui_klines(
			symbol = ticker_base + self.QUOTE,
			interval = self.to_binance_interval(interval),
			end_time = milli_timestamp(end_time),
			limit = limit
		).data()
		if not isinstance(result, list):
			raise self.InvalidResponse

		ans = []
		for arr in result:
			ans.append(Candle(
				ticker_base = ticker_base,
				ticker_quote = self.QUOTE,
				time_opened = int(arr[self.TIME_OPENED]),
				time_closed = int(arr[self.TIME_CLOSED]),
				price_opened = float(arr[self.PRICE_OPENED]),
				price_high = float(arr[self.PRICE_HIGH]),
				price_low = float(arr[self.PRICE_LOW]),
				price_closed = float(arr[self.PRICE_CLOSED]),
				volume = float(arr[self.VOLUME])
			))
		return ans

	def to_binance_interval(self, interval: str) -> UiKlinesIntervalEnum:
		"""Convert a interval string to the respective Binance's enum"""
		for e in UiKlinesIntervalEnum:
			if e.value == interval:
				return e
		raise self.IntervalNotFoundError
