import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime, timedelta
from button import Button
from sensor import Light

GPIO.setmode(GPIO.BCM)


class Blinker:
    def __init__(
        self, channel: int, duration: int=5, off_duration: float=None, initial: bool=True
    ):
        if not off_duration:
            off_duration = duration
        self.duration = timedelta(0, duration)
        self.off_duration = timedelta(0, off_duration)
        self.current = datetime.now()
        self.cycle = initial
        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT, initial=self.get_state(self.cycle))

    def get_next_tick_time(self):
        if self.cycle:
            return self.current + self.duration
        return self.current + self.off_duration

    def tick(self):
        """Switch to the next state depends on set duration."""
        next_cycle = self.get_next_tick_time()
        now = datetime.now()
        if now > next_cycle:
            self.current = datetime.now()
            self.cycle = not self.cycle
            self.turn_on(self.cycle)

    def get_state(self, value: bool) -> int:
        return GPIO.HIGH if not value else GPIO.LOW
    
    def turn_on(self, on: bool=True) -> None:
        GPIO.output(self.channel, self.get_state(on))
        

class PeriodicJob:
    """Change blinker state."""
    
    def __init__(self, channel: int, button_channel: int, sensor_channel: int = 0):
        self.channel = channel
        self.button_channel = button_channel
        self.mode: bool = True
        duration, off_duration = 3, 0.1
        if not self.mode:
            duration, off_duration = off_duration, duration
        self.light = Light(sensor_channel)
        initial = not self.light.detect()
        self.blinker = Blinker(
            channel, duration=duration, off_duration=off_duration, initial=initial
        )
        self.button = Button(button_channel, self.reverse_mode)
        self.welcome()
        self.block_light_sensor = False  # block light detecter when button was used

    def welcome(self):
        print("Welcom message.")
        for _ in range(2):
            self.blinker.turn_on(True)
            sleep(0.4)
            self.blinker.turn_on(False)
            sleep(0.4)

    def reverse_mode(self, value: bool) -> None:
        self.mode = not self.mode
        self.block_light_sensor = True

    def tick(self) -> None:
        now = datetime.now()
        if now.minute % 15 == 0 and now.second <=25:
            self.blinker.tick()
        else:
            if not self.block_light_sensor:
                self.mode = not self.light.detect()
            self.blinker.turn_on(self.mode)


job = PeriodicJob(
    channel=2, 
    button_channel=23, 
    sensor_channel=24,
)

if __name__ == '__main__':
    try:
        while True:
            job.tick()
    finally:
        GPIO.cleanup()

