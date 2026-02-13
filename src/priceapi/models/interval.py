from datetime import datetime, timedelta

class InvalidUnitError(Exception):
		"""Unit suffix is not one of the accepted SUFFIX"""
class InvalidIntervalError(Exception):
	"""The given interval does not follow format"""

class Interval:
	"""A dataclass that represents the interval of a candlesticks

	Constructor takes an interval string in the form of `"[number][unit]"`,
	with the one-letter `unit` and `constraint of number` as follows:
		`s` -- second: `1 <= number <= 60`
		`m` -- minute: `1 <= number <= 60`
		`h` -- hour: `1 <= number <= 24`
		`d` -- day: `1 <= number <= 30`
		`w` -- week: `1 <= number <= 4`
		`M` -- month: `1 <= number <= 12`

	We will not accept month as a unit at the moment.

	Attributes:
		value (str): the inputted string of interval
		delta (timedelta): the timedelta of the interval
		millis (int): the timestamp (by milliseconds) of delta, for convenience.

	Raise:
		ValueError: if `number` cannot be converted to `int`.
		InvalidUnitError: if `unit` is not one of the four.
		InvalidIntervalError: if `number` does not follow the convention.
	"""

	SUFFIX = {
		"s": [60, timedelta(seconds=1)],
		"m": [60, timedelta(minutes=1)],
		"h": [24, timedelta(hours=1)],
		"d": [30, timedelta(days=1)],
		"w": [4, timedelta(weeks=1)],
		"M": [12, timedelta(days=30)],
	}

	def __init__(self, value: str) -> None:
		if len(value) == 0:
			raise ValueError

		self._value = value
		unit = value[-1]
		if unit not in self.SUFFIX:
			raise InvalidUnitError
		limit, self._delta = self.SUFFIX[unit]

		try:
			amount = int(value[:-1])
		except Exception:
			raise InvalidIntervalError("amount is not a number")
		if not 1 <= amount <= limit:
			raise InvalidIntervalError("amount exceeded limit")

		self._delta *= amount
		self._millis = int(self._delta.total_seconds()) * 1000
		pass

	@property
	def value(self) -> str: return self._value
	@property
	def delta(self) -> timedelta: return self._delta
	@property
	def millis(self) -> int: return self._millis

SECOND = Interval("1s")
MINUTE = Interval("1m")
HOUR = Interval("1h")
DAY = Interval("1d")
WEEK = Interval("1w")


def milli_timestamp(time: datetime) -> int:
	"""Convert the datetime to a POSIX timestamp, to the milliseconds.

	Example:
		```
		result = milli_timestamp(datetime.now())
		```
	"""
	MILLIS_IN_SECOND = 1000
	return int(time.timestamp() * MILLIS_IN_SECOND)
def to_datetime(millis: int) -> datetime:
	"""Convert the millis timestamp to a datetime instance.

	Example:
		```
		result = to_datetime(1770635337208)
		# datetime.datetime(2026, 2, 9, 18, 8, 57, 208000)
		```
	"""
	MICROS_IN_MILLIS = 1000
	return datetime.fromtimestamp(millis / MICROS_IN_MILLIS)

def nearest_end_interval(time: datetime, interval: Interval) -> datetime:
	"""Return the nearest finished `end_time` of an interval.

	Seems like all market exchanges' candlesticks chart will yield
	candles with the first (imaginary) candlestick at timestamp 0
	(i.e 1970-01-01T00:00:00Z), thus `start_time % interval.millis == 0`
	and `end_time % interval.millis == interval.millis - 1`
	"""
	timestamp = milli_timestamp(time)
	timestamp = (timestamp + 1) // interval.millis
	timestamp = timestamp * interval.millis - 1
	return to_datetime(timestamp)
