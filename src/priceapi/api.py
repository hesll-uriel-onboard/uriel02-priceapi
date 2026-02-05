from datetime import datetime
import requests
from .models.price import Price

def get_price(coin: str, interval: str, limit: int = 2):
	URL = f"https://api.binance.com/api/v3/klines?symbol={coin}USDT&interval={interval}&limit={limit}"
	req = requests.get(url=URL)
	return [Price(coin, point) for point in req.json()]

def duys_strategy():
	FORMAT = "%H:%M:%S"
	p1, p2 = get_price("BTC", "1m")
	return {
		"time": f"{datetime.fromtimestamp(p1.time_opened).strftime(FORMAT)} -> {datetime.fromtimestamp(p2.time_closed).strftime(FORMAT)}",
		"price": p2.price_closed,
		"coef": p2.price_closed / p1.price_opened
	}

if __name__ == "__main__":
	res = get_price("BTC", "1m")
	print(*res)
