from datetime import datetime
from enum import Enum

class Index(Enum):
	TIME_OPENED = 0
	PRICE_OPENED = 1
	PRICE_HIGH = 2
	PRICE_LOW = 3
	PRICE_CLOSED = 4
	VOLUME = 5
	TIME_CLOSED = 6
class Price:
	def __init__(self, coin_name: str, arr: list) -> None:
		# assert len(arr) == 11
		self.coin_name = coin_name
		self.time_opened: float = float(arr[Index.TIME_OPENED.value]) / 1000
		self.time_closed: float = float(arr[Index.TIME_CLOSED.value]) / 1000
		self.price_opened: float = float(arr[Index.PRICE_OPENED.value])
		self.price_closed: float = float(arr[Index.PRICE_CLOSED.value])
		self.price_high: float  = float(arr[Index.PRICE_HIGH.value])
		self.price_low: float = float(arr[Index.PRICE_LOW.value])

	def __str__(self) -> str:
		FORMAT = "%H:%M:%S"
		time_data = "->".join([
			f"{datetime.fromtimestamp(self.time_opened).strftime(FORMAT)}",
			f"{datetime.fromtimestamp(self.time_closed).strftime(FORMAT)}",
		])
		price_data = " ".join([
			f"o {self.price_opened}",
			f"l {self.price_low}",
			f"h {self.price_high}",
			f"c {self.price_closed}",
		])
		return f"{self.coin_name}[{time_data} | {price_data}]"
