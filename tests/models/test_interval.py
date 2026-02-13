from priceapi.service import milli_timestamp
import pytest
from datetime import datetime, timedelta
import random
from priceapi.models.interval import MINUTE, Interval, InvalidUnitError, InvalidIntervalError, nearest_end_interval, to_datetime
random.seed(datetime.now().timestamp())

@pytest.mark.parametrize("interval_string, expected_delta", [
	("1s", timedelta(seconds = 1)),
	("15m", timedelta(minutes = 15)),
	("2h", timedelta(hours = 2)),
	("3d", timedelta(days = 3)),
	("1w", timedelta(weeks = 1)),
	("1M", timedelta(days = 30)),
])
def test_valid_intervals(interval_string: str, expected_delta: timedelta):
	interval = Interval(interval_string)
	assert interval.delta == expected_delta
	assert interval.millis == milli_timestamp(datetime.fromtimestamp(0) + expected_delta)

@pytest.mark.parametrize("interval_string", ["1k", "2x"])
def test_invalid_unit_error(interval_string):
	with pytest.raises(InvalidUnitError):
		Interval(interval_string)

@pytest.mark.parametrize("interval_string", ["0s", "0m", "0h", "0d", "0w", "0m"])
def test_zero_error(interval_string):
	with pytest.raises(InvalidIntervalError):
		Interval(interval_string)

@pytest.mark.parametrize("interval_string", ["61s", "61m", "25h", "31d", "5w", "13M"])
def test_number_too_large_error(interval_string):
	with pytest.raises(InvalidIntervalError):
		Interval(interval_string)

@pytest.mark.parametrize("interval_string", ["as", "6em", "!!h"])
def test_not_a_number(interval_string):
	with pytest.raises(InvalidIntervalError):
		Interval(interval_string)


@pytest.mark.parametrize("time, interval", [
	(to_datetime(100*1000), MINUTE),
	(to_datetime(60*1000-1), MINUTE),
])
def test_nearest_end_interval(time: datetime, interval: Interval):
	result = nearest_end_interval(time, interval)
	print(milli_timestamp(time), interval.millis, milli_timestamp(result), result.timestamp())
	assert milli_timestamp(result) > 0
	assert milli_timestamp(result) % interval.millis == interval.millis - 1
	assert result + interval.delta > time
