import RPi.GPIO as GPIO
from collections import deque
from datetime import datetime, timedelta
from time import time


class Light:
    HISTORY_SIZE = 2
    TIME_SWITCH_SECONDS = 60*5
    time_to_switch = timedelta(0, TIME_SWITCH_SECONDS)
    def __init__(self, channel: int):
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN)
        self.state = self.is_on()
        self.last_check = datetime.now()
        self.history = deque([self.is_on()]*self.HISTORY_SIZE, maxlen=self.HISTORY_SIZE)

    def is_on(self) -> bool:
        return GPIO.input(self.channel) == GPIO.LOW

    def detect(self):
        state = self.is_on()
        now = datetime.now()
        if all([item is state for item in self.history]):
            self.state = state
        if now > self.last_check + self.time_to_switch:
            self.last_check = now
            self.history.append(state)
        return self.state


if __name__ == '__main__':
    light = Light(24)
    try:
        while True:
            print(light.is_on())
            time.sleep(1)
    finally:
        GPIO.cleanup()
