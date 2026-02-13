from abc import ABC, abstractmethod
from datetime import datetime
from typing import override

from binance_common.errors import BadRequestError
from binance_sdk_spot.rest_api.rest_api import UiKlinesIntervalEnum
from binance_sdk_spot import Spot

from .models.candle import Candle
from .models.interval import Interval, InvalidUnitError, milli_timestamp

class InvalidParameterError(Exception):
	"""Invalid parameter"""
class InvalidResponseError(Exception):
	"""The market exchange server failed to return a valid response"""

class ServiceInterface(ABC):
	"""An abstract interface of functionalities, that adapts for every market exchange.

	Example:
		```python
		market: ServiceInterface = BinanceService()
		result = market.get_finished_candles("BTCUSDT", "1m", datetime.now(), 2)
		```
	"""

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
	PRICE_HIGHEST: int = 2
	PRICE_LOWEST: int = 3
	PRICE_CLOSED: int = 4
	VOLUME: int = 5
	TIME_CLOSED: int = 6

	def __init__(self, **kwargs) -> None:
		super().__init__()
		FAKE = "_fake_engine"
		if FAKE in kwargs:
			self.engine = kwargs[FAKE]
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
				raise InvalidResponseError("No status code found.")

			code = -e.status_code
			if code // 100 == 11:	# -11xx: invalid request
				raise InvalidParameterError(e.error_message)
			else:
				raise InvalidResponseError(e.error_message)
		except Exception:
			raise InvalidResponseError("Unknown reason.")

		if not isinstance(result, list):
			raise InvalidResponseError("The return response is not a list")
		if len(result) > limit:
			raise InvalidResponseError("The return response is not a list")

		ans = []
		for arr in result:
			ans.append(Candle(
				base_ticker = ticker_base,
				quote_ticker = ticker_quote,
				opening_time = int(arr[self.TIME_OPENED]),
				closing_time = int(arr[self.TIME_CLOSED]),
				open_price = float(arr[self.PRICE_OPENED]),
				high_price = float(arr[self.PRICE_HIGHEST]),
				low_price = float(arr[self.PRICE_LOWEST]),
				close_price = float(arr[self.PRICE_CLOSED]),
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
			except InvalidUnitError:
				pass
		raise InvalidParameterError(f"No such interval as {interval.value}.")
