from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from types import NotImplementedType

from binance_sdk_spot.rest_api.rest_api import UiKlinesIntervalEnum

from .models.price import Price
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
	return datetime.fromtimestamp(millis / 1000.0)

class CoinInterface(ABC):
	BASE_COIN = "USDT"
	class InvalidResponse(Exception):
		pass

	@abstractmethod
	def get_finished_candles(self,
		coin_name: str,
		interval: str,
		end_time: datetime,
		limit: int = 2
	) -> list[Price]:
		"""Return the last `limit` **finished** candles

		Example:
		```
		result = engine.get_finished_candles(end_time = datetime.now())
		```

		TODO:
			Implement this function in the adapters

		"""
		raise NotImplementedError

class BinanceAdapter(CoinInterface):
	class IntervalNotFoundError(Exception):
		pass
	TIME_OPENED = 0
	PRICE_OPENED = 1
	PRICE_HIGH = 2
	PRICE_LOW = 3
	PRICE_CLOSED = 4
	VOLUME = 5
	TIME_CLOSED = 6

	def __init__(self) -> None:
		super().__init__()
		self.engine = Spot()

	def get_finished_candles(self,
		coin_name: str,
		interval: str,
		end_time: datetime = datetime.now(),
		limit: int = 2
	) -> list[Price]:
		result = self.engine.rest_api.ui_klines(
			symbol = coin_name + self.BASE_COIN,
			interval = self.to_binance_interval(interval),
			end_time = milli_timestamp(end_time),
			limit = limit
		).data()
		if not isinstance(result, list):
			raise self.InvalidResponse

		ans = []
		for arr in result:
			ans.append(Price(
				coin_name = coin_name,
				time_opened = int(arr[self.TIME_OPENED]),
				time_closed = int(arr[self.TIME_CLOSED]),
				price_opened = float(arr[self.PRICE_OPENED]),
				price_high = float(arr[self.PRICE_HIGH]),
				price_low = float(arr[self.PRICE_LOW]),
				price_closed = float(arr[self.PRICE_CLOSED]),
			))
		return ans

	def to_binance_interval(self, interval: str) -> UiKlinesIntervalEnum:
		for e in UiKlinesIntervalEnum:
			if e.value == interval:
				return e
		raise self.IntervalNotFoundError
