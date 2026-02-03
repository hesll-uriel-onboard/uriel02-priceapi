import requests
from models.price import Price

def get_price(coin: str, interval: str, limit: int = 2):
	URL = f"https://api.binance.com/api/v3/klines?symbol={coin}USDT&interval={interval}&limit={limit}"
	req = requests.get(url=URL)
	return [Price(coin, point) for point in req.json()]

if __name__ == "__main__":
	res = get_price("BTC", "1m")
	print(*res)
