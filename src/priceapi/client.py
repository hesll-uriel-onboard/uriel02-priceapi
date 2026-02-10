from datetime import datetime
from enum import Enum

from .models.candle import Candle
from .service import BinanceService, milli_timestamp, to_datetime
from .models.interval import Interval, MINUTE

class ClientProvider(Enum):
	"""Enum of Service constructors"""
	BINANCE = BinanceService

class Client():
	"""An interface for client to request and retrieve information from market exchange."""

	NON_ALNUM = "".join([chr(c) \
		for c in range(33, 126+1) \
		if not chr(c).isalnum()])
	@staticmethod
	def split_symbols(symbols: str) -> tuple[str, str]:
		for i, ch in enumerate(symbols):
			if not ch.isalnum():
				base, quote = symbols[:i], symbols[i+1:]
				if base == "" or quote == "":
					raise ValueError("Base and Quote ticker must not be empty")
				return base, quote
		raise ValueError("No separators found")
	@staticmethod
	def nearest_minute(time: datetime) -> datetime:
		timestamp = milli_timestamp(time)
		timestamp -= timestamp % MINUTE.millis + 1
		return to_datetime(timestamp)

	def get_finished_candles(self,
		asset_pair: str,
		interval: str,
		end_time: datetime,
		limit: int = 2,
		provider: ClientProvider = ClientProvider.BINANCE,
	) -> list[Candle]:
		"""Return finished candlesticks of the market data of an asset pair.

		A finished candle is a candle of which its data is already finalised,
		i.e. its end_time is in the past.

		Args:
			asset_pair: a pair of ticker symbols.
				the format should be "[ticker1][non-alnum separator][ticker2]"
				(e.g. "BTC-USDT", "BTC/USDT")
			interval: the duration recorded of each candlestick,
				with the format [duration][length symbol],
				e.g. "1m" (1 min), "30d" (30 days), "1M" (one month).
			end_time: the time threshold that every candle records.
			limit: at most how many records are shown.
			provider: which service will run the request

		Returns:
			A list of finished candles. Each Price instance consists of
			asset pair symbol, the opened/closed timestamp, and OHLCV.

		Raise:
			NotImplementedError: if a MarketInterface class hasn't implemented this method
			ArgumentError: if `asset_pair` or `interval` is invalid
		"""

		print(asset_pair, self.NON_ALNUM)
		base, quote = self.split_symbols(asset_pair)
		end_time = self.nearest_minute(end_time)

		service = (provider.value)()
		return service.get_finished_candles(
			ticker_base = base,
			ticker_quote = quote,
			interval = Interval(interval),
			end_time = end_time,
			limit = limit
		)
