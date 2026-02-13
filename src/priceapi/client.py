from datetime import datetime
from enum import Enum

from .models.candle import Candle
from .service import BinanceService
from .models.interval import Interval, nearest_end_interval

class ClientProvider(Enum):
	"""Enum of Service constructors"""
	BINANCE = BinanceService

class Client():
	"""An interface for client to request and retrieve information from market exchange."""

	# non-alnum printable characters
	NON_ALNUM = "".join([chr(c) \
		for c in range(33, 126+1) \
		if not chr(c).isalnum()])

	@staticmethod
	def split_symbols(symbols: str) -> tuple[str, str]:
		"""Split symbols to a pair of symbol.

		Args:
			symbols(str): sees `asset_pair` in `get_finished_candles`.

		Returns:
			a pair of two string, the first one is the base asset,
			the second one is the quote asset.

		Examples:
			```python
			base, quote = Client.split_symbols("BTC?USDT")
			assert base == "BTC" and quote == "USDT"
			```

		Raise:
			ValueError: if `symbols` can not be parsed.
		"""
		for i, ch in enumerate(symbols):
			if not ch.isalnum():
				base, quote = symbols[:i], symbols[i+1:]
				if base == "" or quote == "":
					raise ValueError("Base and Quote ticker must not be empty")
				return base, quote
		raise ValueError("No separators found")

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
			NotImplementedError:
				if a MarketInterface class hasn't implemented this method
			priceapi.service.ServiceInterface.InvalidParameterError:
				if the passed parameter(s) is invalid
			priceapi.service.ServiceInterface.InvalidResponseError:
				if the server cannot return a valid response
				(according to the Returns' requirements)
		"""

		base, quote = self.split_symbols(asset_pair)
		real_interval: Interval = Interval(interval)
		end_time = nearest_end_interval(end_time, real_interval)

		service = (provider.value)()
		return service.get_finished_candles(
			ticker_base = base,
			ticker_quote = quote,
			interval = real_interval,
			end_time = end_time,
			limit = limit
		)
