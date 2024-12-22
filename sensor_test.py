import sys
from unittest.mock import MagicMock 
sys.modules['RPi.GPIO'] = MagicMock()
from sensor import Light
from datetime import datetime, timedelta
from collections import deque

class TestLight(Light):
    HISTORY_SIZE = 2
    default_state_test = True
    def __init__(self, channel: int):
        self.last_check = datetime.now()
        super().__init__(channel)

    def is_on(self) -> bool:
        return self.default_state_test


def test_ignore_state_change():
    now = datetime.now()
    light = TestLight(23)
    light.state = False
    light.history = [False, False]
    light.default_state_test = True
    last_check = light.last_check
    assert light.detect() is False
    assert light.detect() is False
    assert last_check == light.last_check

def test_state_change():
    now = datetime.now()
    light = TestLight(23)
    light.state = False
    light.history = [False, False]
    light.default_state_test = True
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    last_check = light.last_check
    assert light.detect() is False
    light.history = [True, True]
    assert light.detect() is True
    assert last_check != light.last_check

def test_state_change_ignore():
    now = datetime.now()
    light = TestLight(23)
    light.state = False
    light.history = deque([False, False], maxlen=light.HISTORY_SIZE)
    light.default_state_test = False
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    last_check = light.last_check
    assert light.detect() is False, "ignore same state change"
    assert light.detect() is False
    assert last_check != light.last_check
    light.default_state_test = True
    light.history = deque([False, True], maxlen=light.HISTORY_SIZE)
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    assert light.detect() is False, "undefined state"
    assert [*light.history] == [True, True]
    assert light.detect() is True, "state change in the next tick"

def test_day_to_night():
    now = datetime.now()
    light = TestLight(23)
    light.state = False
    light.default_state_test = True
    light.history = deque([False, False], maxlen=light.HISTORY_SIZE)
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    assert light.detect() is False
    assert [*light.history] == [False, True]
    assert light.detect() is False, "ignore next tick"
    assert [*light.history] == [False, True]
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    assert light.detect() is False
    assert [*light.history] == [True, True]
    light.last_check = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    assert light.detect() is True
    assert [*light.history] == [True, True]


if __name__ == '__main__':
    test_ignore_state_change()
    test_state_change()
    test_state_change_ignore()
    test_day_to_night()
    print("DONE.")