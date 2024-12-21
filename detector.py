import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from time import time


class Light:
    TIME_SWITCH_SECONDS = 60*5
    time_to_switch = timedelta(0, TIME_SWITCH_SECONDS)
    def __init__(self, channel: int):
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN)
        self.was_on = self.is_on()
        self.last_change = datetime.now()

    def is_on(self) -> bool:
        return GPIO.input(self.channel) == GPIO.LOW

    def is_on_for_long_time(self):
        is_on = self.is_on()
        now = datetime.now()
        state = self.was_on
        if now > self.last_change + self.time_to_switch and self.was_on != is_on:
            self.was_on = is_on
            self.last_change = now
        return state


if __name__ == '__main__':
    light = Light(24)
    try:
        while True:
            print(light.is_on())
            time.sleep(1)
    finally:
        GPIO.cleanup()
