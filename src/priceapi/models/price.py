from datetime import datetime

class Price:
	def __init__(self,
		coin_name: str,
		time_opened: int,
		time_closed: int,
		price_opened: float,
		price_closed: float,
		price_high: float,
		price_low: float,
	) -> None:
		# assert len(arr) == 11
		self.coin_name = coin_name
		self.time_opened = time_opened
		self.time_closed = time_closed
		self.price_opened = price_opened
		self.price_high = price_high
		self.price_low = price_low
		self.price_closed = price_closed

	def __str__(self) -> str:
		FORMAT = "%H:%M:%S"
		time_data = "->".join([
			f"{datetime.fromtimestamp(self.time_opened / 1000.0).strftime(FORMAT)}",
			f"{datetime.fromtimestamp(self.time_closed / 1000.0).strftime(FORMAT)}",
		])
		price_data = " ".join([
			f"o {self.price_opened}",
			f"l {self.price_low}",
			f"h {self.price_high}",
			f"c {self.price_closed}",
		])
		return f"{self.coin_name}[{time_data} | {price_data}]"
