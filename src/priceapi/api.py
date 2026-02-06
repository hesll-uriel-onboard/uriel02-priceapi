from datetime import datetime
import requests
from .models.price import Price
from .adapter import CoinInterface, BinanceAdapter, to_datetime
# def get_price(coin: str, interval: str, end_time: datetime, limit: int = 2) -> list[Price]:
# 	timestamp = int(end_time.timestamp() * 1000) # milli
# 	URL = f"https://api.binance.com/api/v3/klines?symbol={coin}USDT&interval={interval}&limit={limit}&endTime={timestamp}"
# 	req = requests.get(url=URL, timeout=5)
# 	return [Price(coin, point) for point in req.json()]
engine: CoinInterface = BinanceAdapter()

def duys_strategy(end_time: datetime) -> dict[str, str]:
	FORMAT = "%H:%M:%S"
	p1, p2 = engine.get_finished_candles("BTC", "1m", end_time)
	return {
		"time": f"{to_datetime(p1.time_opened).strftime(FORMAT)} -> {to_datetime(p2.time_closed).strftime(FORMAT)}",
		"price": str(p2.price_closed),
		"coef": str(p2.price_closed / p1.price_opened)
	}

if __name__ == "__main__":
	res = duys_strategy(datetime.now())
	print(*res)
