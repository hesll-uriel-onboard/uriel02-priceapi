from datetime import datetime
from .adapter import ServiceInterface, BinanceService, to_datetime

engine: ServiceInterface = BinanceService()

def duys_strategy(end_time: datetime) -> dict[str, str]:
	"""Retrieve the last two finished candles, and return the ratio between the
	opening price of the previous candle and the closing price of the last candle.

	Args:
		end_time: limits the closing time of the candles to be not later than the value of this parameter.

	Returns:
		A dict contains the following information:
			"time": a formatted string of the opening and closing time of the two candles.
			"price": the closing price of the last finished candle.
			"ratio": the aforementioned ratio.

	"""
	FORMAT = "%H:%M:%S"
	p1, p2 = engine.get_finished_candles("BTC", "1m", end_time)
	return {
		"time": f"{to_datetime(p1.time_opened).strftime(FORMAT)} \
		-> {to_datetime(p2.time_closed).strftime(FORMAT)}",
		"price": str(p2.price_closed),
		"ratio": str(p2.price_closed / p1.price_opened)
	}

if __name__ == "__main__":
	res = duys_strategy(datetime.now())
	print(*res)
