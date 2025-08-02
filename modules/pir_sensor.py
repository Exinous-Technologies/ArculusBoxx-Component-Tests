# pir_sensor_test.py

import RPi.GPIO as GPIO
import time

class PIRSensorTest:
    """
    PIR motion sensor tester.

    Raises a RuntimeError if the sensor never stabilizes LOW after power-up
    (e.g. not connected or stuck HIGH).  Motion detection then only passes
    when there's real, wired-up motion.
    """

    def __init__(self, pin: int, calibration_delay: float = 2.0):
        """
        Initialize the PIR sensor on the given BCM pin.

        :param pin: BCM pin number where PIR OUT is wired.
        :param calibration_delay: how long the PIR needs to stabilize on power-up.
        """
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        # use an internal pull-down so floating = LOW
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Give the sensor time to calibrate, then verify it ever goes LOW.
        time.sleep(calibration_delay)
        if GPIO.input(self.pin):
            raise RuntimeError(
                f"PIR output stuck HIGH after {calibration_delay}s on pin {self.pin} — "
                "check your wiring or that the sensor is plugged in."
            )

    def detect_motion(self, timeout: float = 10.0, poll_interval: float = 0.1) -> bool:
        """
        Block until motion is detected or timeout is reached.

        :param timeout: max seconds to wait for motion
        :param poll_interval: how often to sample the sensor
        :return: True if motion was detected, False otherwise
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            if GPIO.input(self.pin):
                return True
            time.sleep(poll_interval)
        return False

    def cleanup(self):
        """
        Clean up this sensor's GPIO pin.
        """
        GPIO.cleanup(self.pin)
