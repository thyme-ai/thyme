from app.functions.gcal.helpers.datetime import get_datetime_object
from app.functions.thyme.helpers.conflict_avoidance import get_suggested_start_time
import pytest

#         0      1    2      3    4      5    6
HOURS = ['07', '08', '09', '10', '12', '17', '18']
TIMES = list(map(lambda hour: f'{hour}:00:00', HOURS))
DAY = '2024-06-01'
TIMEZONE = '-07:00'
dt = list(map(lambda t: get_datetime_object(f'{DAY}T{t}{TIMEZONE}'), TIMES))

IDEAL_STARTS = [ dt[1], dt[3] ]
IDEAL_ENDS = [ dt[2], dt[4]  ]
AWAKE_RANGE = {"start": dt[0], "end": dt[5]}

BUSY_RANGES = [
    { "start": dt[1], "end": dt[2] },
    { "start": dt[3], "end": dt[4] },
]

BUSY_RANGES_FULLY_BOOKED_DAY = [
    { "start": dt[0], "end": dt[5] },
]


# @pytest.mark.skip
def test_get_suggested_start_time_when_time_is_busy_1():
    suggested_start_time = get_suggested_start_time(dt[1], dt[2], AWAKE_RANGE, BUSY_RANGES)
    assert suggested_start_time == dt[0] or suggested_start_time == dt[2]


# @pytest.mark.skip
def test_get_suggested_start_time_when_time_is_busy_2():
    suggested_start_time = get_suggested_start_time(dt[3], dt[4], AWAKE_RANGE, BUSY_RANGES)
    assert suggested_start_time == dt[2] or suggested_start_time == dt[4]


# @pytest.mark.skip
def test_get_suggested_start_time_when_time_is_free():
    suggested_start_time = get_suggested_start_time(dt[0], dt[1], AWAKE_RANGE, BUSY_RANGES)
    assert suggested_start_time == dt[0]


# @pytest.mark.skip
def test_get_suggested_start_time_only_available_time_is_outside_awake_hours():
    suggested_start_time = get_suggested_start_time(dt[5], dt[6], AWAKE_RANGE, BUSY_RANGES_FULLY_BOOKED_DAY)
    assert suggested_start_time == None