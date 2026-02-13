from datetime import datetime

from .models.candle import Candle
from .models.interval import to_datetime
from .client import Client

engine = Client()

def _duys_strategy(candles: list[Candle]) -> dict[str, str] | None:
	"""Return the ratio between the opening price of the previous candle
	and the closing price of the last candle.

	Args:
		end_time: limits the closing time of the candles to be
			not later than the value of this parameter.

	Returns:
		If there exists two candles as such, returns a dict contains the following information:
			"time": a formatted string of the opening and closing time of the two candles.
			"price": the closing price of the last finished candle.
			"ratio": the aforementioned ratio.
		Otherwise, returns None.
	"""
	if len(candles) < 2:
		return None

	p1, p2 = candles[0], candles[1]
	FORMAT = "%H:%M:%S"
	return {
		"time": f"{to_datetime(p1.opening_time).strftime(FORMAT)} -> {to_datetime(p2.closing_time).strftime(FORMAT)}",
		"price": str(p2.close_price),
		"ratio": str(p2.close_price / p1.open_price)
	}

def duys_strategy(end_time: datetime) -> dict[str, str] | None:
	"""Retrieve the last two finished candles, and runs _duys_strategy."""
	result = engine.get_finished_candles("BTC/USDT", "1m", end_time)
	return _duys_strategy(result)

if __name__ == "__main__":
	res = duys_strategy(datetime.now())
	if res is None:
		print("failed")
	else:
		print(*res)
