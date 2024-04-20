import RPi.GPIO as GPIO
from time import sleep, time
from datetime import datetime, timedelta


class Button:
    def __init__(self, channel, release_callback):
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.is_press = False
        self.is_pressed = False
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.edge_detected)
        self.callback_for_press = []
        self.callback_for_release = [release_callback]
        self.last_change = None
        self.is_last_stable = False
        self.press_time = 0
        self.release_time = 0

    def check_stable_press():
        #TODO: make it work
        if not self.last_change:
            self.last_change = datetime.now().timestamp()
        now = datetime.now()
        is_stable = now.timestamp() - self.last_change > 0.8
        if is_stable:
            self.is_last_stable = True
            self.last_change = now
        return is_stable

    def reset(self):
        self.is_pressed = False

    def edge_detected(self, value):
        is_release = GPIO.input(self.channel) == GPIO.HIGH
        if self.is_switch_bounce(is_release):
            return
        if is_release:
            self.release()
        else:
            self.press()
        try:
            set_mode(is_release)
        except Exception as e:
            print(f"ERROR: {e}")

    def press(self):
        self.is_pressed = False
        self.is_press = True
        for cb in self.callback_for_press:
            cb(self)

    def release(self):
        self.is_pressed = True
        self.is_press = False
        for cb in self.callback_for_release:
            cb(self)

    def is_switch_bounce(self, is_release=True):
        """Check if the switch is in a bouncing state within a specific timeframe."""
        now = time()
        if is_release:
            bounce_time = self.release_time
            self.release_time = now
        else:
            bounce_time = self.press_time
            self.press_time = now
        is_bounce = (now - bounce_time) < 0.5
        print('is_bounce', is_bounce, now - bounce_time)
        return is_bounce


if __name__ == '__main__':
    button = Button(2)
    try:
        while True:
            #button.tick()
            print(button.is_pressed, '-', button.is_press)
            time.sleep(1)
    finally:
        GPIO.cleanup()
