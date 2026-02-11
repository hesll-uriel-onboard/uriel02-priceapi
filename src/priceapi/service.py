from abc import ABC, abstractmethod
from datetime import datetime
from typing import override

from binance_common.errors import BadRequestError
from binance_sdk_spot.rest_api.rest_api import UiKlinesIntervalEnum

from .models.candle import Candle
from .models.interval import Interval
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

	class InvalidParameterError(Exception):
		"""Invalid parameter"""
	class InvalidResponseError(Exception):
		pass


	QUOTE = "USDT"

	@abstractmethod
	def get_finished_candles(self,
		ticker_base: str,
		ticker_quote: str,
		interval: Interval,
		end_time: datetime,
		limit: int = 2,
		**kwargs
	) -> list[Candle]:
		"""Return the last `limit` **finished** candles.

		See `priceapi.client.Client.get_finished_candles(self, asset_pair, interval, end_time, limit, provider)`.

		Example:
		```
		result = service.get_finished_candles(end_time = datetime.now())
		```

		TODO:
			Implement this function in the adapters
		"""
		raise NotImplementedError

class BinanceService(ServiceInterface):
	"""Implementation of ServiceInterface for Binance"""

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
		ticker_quote: str,
		interval: Interval,
		end_time: datetime,
		limit: int = 2,
		**kwargs
	) -> list[Candle]:
		"""See base class."""
		binance_interval = self.to_binance_interval(interval)
		try:
			result = self.engine.rest_api.ui_klines(
				symbol = ticker_base + ticker_quote,
				interval = binance_interval,
				end_time = milli_timestamp(end_time),
				limit = limit
			).data()
		except BadRequestError as e:
			if e.status_code is None:
				raise self.InvalidResponseError("No status code found.")

			code = -e.status_code
			if code // 100 == 11:	# -11xx: invalid request
				raise self.InvalidParameterError(e.error_message)
			else:
				raise self.InvalidResponseError(e.error_message)
		except Exception:
			raise self.InvalidResponseError("Unknown reason.")

		if not isinstance(result, list):
			raise self.InvalidResponseError("The return response is not a list")
		if len(result) > limit:
			raise self.InvalidResponseError("The return response is not a list")

		ans = []
		for arr in result:
			ans.append(Candle(
				ticker_base = ticker_base,
				ticker_quote = ticker_quote,
				time_opened = int(arr[self.TIME_OPENED]),
				time_closed = int(arr[self.TIME_CLOSED]),
				price_opened = float(arr[self.PRICE_OPENED]),
				price_high = float(arr[self.PRICE_HIGH]),
				price_low = float(arr[self.PRICE_LOW]),
				price_closed = float(arr[self.PRICE_CLOSED]),
				volume = float(arr[self.VOLUME])
			))
		return ans

	def to_binance_interval(self, interval: Interval) -> UiKlinesIntervalEnum:
		"""Convert a interval string to the respective Binance's enum"""
		print("here")
		for e in UiKlinesIntervalEnum:
			try:
				if Interval(e.value).millis == interval.millis:
					print(e)
					return e
			except Interval.InvalidUnitError:
				pass
		raise self.InvalidParameterError(f"No such interval as {interval.value}.")
