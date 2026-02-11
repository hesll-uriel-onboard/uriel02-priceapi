from datetime import datetime
from .service import to_datetime
from .client import Client

engine = Client()

def duys_strategy(end_time: datetime) -> dict[str, str] | None:
	"""Retrieve the last two finished candles, and return the ratio between the
	opening price of the previous candle and the closing price of the last candle.

	Args:
		end_time: limits the closing time of the candles to be not later than the value of this parameter.

	Returns:
		If there exists two candles as such, returns a dict contains the following information:
			"time": a formatted string of the opening and closing time of the two candles.
			"price": the closing price of the last finished candle.
			"ratio": the aforementioned ratio.
		Otherwise, returns None.
	"""
	FORMAT = "%H:%M:%S"
	result = engine.get_finished_candles("BTC/USDT", "1m", end_time)
	if len(result) < 2:
		return None

	p1, p2 = result
	return {
		"time": f"{to_datetime(p1.time_opened).strftime(FORMAT)} -> {to_datetime(p2.time_closed).strftime(FORMAT)}",
		"price": str(p2.price_closed),
		"ratio": str(p2.price_closed / p1.price_opened)
	}

if __name__ == "__main__":
	res = duys_strategy(datetime.now())
	if res is None:
		print("failed")
	else:
		print(*res)
