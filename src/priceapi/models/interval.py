from datetime import timedelta


class Interval:
	"""A dataclass that represents the interval of a candlesticks

	Constructor takes an interval string in the form of `"[number][unit]"`,
	with the one-letter `unit` and `constraint of number` as follows:
		`s` -- second: `number == 1`
		`m` -- minute: `1 <= number <= 59`
		`h` -- hour: `1 <= number <= 23`
		`d` -- day: `1 <= number <= 30`
		`w` -- week: `number == 1`
		`M` -- month: `number == 1`

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

	class InvalidUnitError(Exception):
		"""Unit suffix is not one of the accepted SUFFIX"""
	class InvalidIntervalError(Exception):
		"""The given interval does not follow format"""
	SUFFIX = {
		"s": [1, timedelta(seconds=1)],
		"m": [59, timedelta(minutes=1)],
		"h": [23, timedelta(hours=1)],
		"d": [30, timedelta(days=1)],
		"w": [1, timedelta(weeks=1)],
		"M": [1, timedelta(days=30)],
	}

	def __init__(self, value: str) -> None:
		if len(value) == 0:
			raise ValueError

		self._value = value
		unit = value[-1]
		if unit not in self.SUFFIX:
			raise self.InvalidUnitError
		limit, self._delta = self.SUFFIX[unit]

		try:
			amount = int(value[:-1])
		except Exception:
			raise ValueError
		if not 1 <= amount <= limit:
			raise self.InvalidIntervalError

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
