from dataclasses import dataclass
from datetime import datetime

@dataclass
class Candle:
	"""Information of a candle.

	Attributes:
		ticket_base: the symbol of the ticker that is exchanged from.
		ticket_quote: the symbol of the ticker that is exchanged to.
		time_opened: the opening time of a candle
		time_closed: the closing time of a candle.
		price_opened, price_high, price_low, price_closed, volume: respective to OHLCV.
	"""

	base_ticker: str
	quote_ticker: str
	opening_time: int
	closing_time: int
	open_price: float
	high_price: float
	low_price: float
	close_price: float
	volume: float

	def __str__(self) -> str:
		FORMAT = "%H:%M:%S"
		time_data = "->".join([
			f"{datetime.fromtimestamp(self.opening_time / 1000.0).strftime(FORMAT)}",
			f"{datetime.fromtimestamp(self.closing_time / 1000.0).strftime(FORMAT)}",
		])
		price_data = " ".join([
			f"o {self.open_price}",
			f"l {self.low_price}",
			f"h {self.high_price}",
			f"c {self.close_price}",
		])
		return f"{self.base_ticker}/{self.quote_ticker}[{time_data} | {price_data}]"
