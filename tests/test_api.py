from datetime import datetime
from priceapi.api import duys_strategy

def test_OK():
	assert duys_strategy(datetime.now()) is not None

def test_empty():
	# somehow Spot.rest_api.ui_klines does not allow end_time to be 0.
	assert duys_strategy(datetime.fromtimestamp(1000)) is None
