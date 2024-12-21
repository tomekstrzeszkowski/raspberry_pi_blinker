import sys
from unittest.mock import MagicMock 
sys.modules['RPi.GPIO'] = MagicMock()
from detector import Light
from datetime import datetime, timedelta

class TestLight(Light):
    default_state_test = True
    def __init__(self, channel: int):
        self.channel = channel
        self.was_on = self.is_on()
        self.last_change = datetime.now()

    def is_on(self) -> bool:
        return self.default_state_test


def test_ignore_state_change():
    now = datetime.now()
    light = TestLight(23)
    light.was_on = False
    light.default_state_test = True
    last_change = light.last_change
    assert light.is_on_for_long_time() is False
    assert light.is_on_for_long_time() is False
    assert last_change == light.last_change

def test_state_change():
    now = datetime.now()
    light = TestLight(23)
    light.was_on = False
    light.default_state_test = True
    light.last_change = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    last_change = light.last_change
    assert light.is_on_for_long_time() is False
    assert light.is_on_for_long_time() is True
    assert last_change != light.last_change

def test_state_change_ignore():
    now = datetime.now()
    light = TestLight(23)
    light.was_on = False
    light.default_state_test = False
    light.last_change = now - timedelta(0, light.TIME_SWITCH_SECONDS + 1)
    last_change = light.last_change
    assert light.is_on_for_long_time() is False, "ignore same state change"
    assert light.is_on_for_long_time() is False
    assert last_change == light.last_change
    light.default_state_test = True
    assert light.is_on_for_long_time() is False, "state changed but waiting for next tick"
    assert light.is_on_for_long_time() is True, "state change in the next tick"

if __name__ == '__main__':
    test_ignore_state_change()
    test_state_change()
    test_state_change_ignore()