from datetime import datetime, timedelta
import random
from priceapi.models.interval import Interval, SECOND, MINUTE, HOUR, DAY
random.seed(datetime.now().timestamp())

def test_valid_unit():
	assert SECOND.delta == timedelta(seconds=1) and SECOND.millis == 1000
	assert MINUTE.delta == timedelta(minutes=1) and MINUTE.millis == 1000 * 60
	assert HOUR.delta == timedelta(hours=1) and HOUR.millis == 1000 * 60 * 60
	assert DAY.delta == timedelta(days=1) and DAY.millis == 1000 * 60 * 60 * 24

def test_arbitrary_interval():
	for unit, delta in [
		["s", timedelta(seconds=1)],
		["m", timedelta(minutes=1)],
		["h", timedelta(hours=1)],
		["d", timedelta(days=1)],
	]:
		limit = Interval.SUFFIX[unit][0]
		number = random.randint(1, limit)
		interval_value = str(number) + unit
		interval_delta: timedelta = delta * number
		interval_millis = interval_delta.total_seconds() * 1000

		interval = Interval(interval_value)
		assert interval.delta == interval_delta
		assert interval.millis == interval_millis

def test_invalid_unit_error():
	try:
		Interval("1k")
	except Interval.InvalidUnitError:
		assert True
	else:
		assert False

def test_invalid_interval_error():
	for unit, delta in [
		["s", timedelta(seconds=1)],
		["m", timedelta(minutes=1)],
		["h", timedelta(hours=1)],
		["d", timedelta(days=1)],
	]:
		number = Interval.SUFFIX[unit][0] + 1
		interval_value = str(number) + unit
		print(interval_value)
		try:
			Interval(interval_value)
		except Interval.InvalidIntervalError:
			assert True
		else:
			assert False
