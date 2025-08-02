"""
relay.py — Importable module for Raspberry Pi relay control
"""
import RPi.GPIO as GPIO
import time

__all__ = ["Relay"]

class Relay:
    """
    Context-managed class for controlling a single-channel relay on a Raspberry Pi.
    Usage:
        from relay import Relay
        with Relay(pin=17) as relay:
            relay.on()
            # ...do other work...
            relay.off()
    """
    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.HIGH)

    def __enter__(self) -> "Relay":
        return self

    def on(self) -> None:
        """
        Energize the relay (close the circuit).
        """
        GPIO.output(self.pin, GPIO.LOW)

    def off(self) -> None:
        """
        De-energize the relay (open the circuit).
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def test(self, duration: float = 2.0) -> None:
        """
        Run a simple on-for-duration then off sequence.
        :param duration: seconds to keep the relay on.
        """
        self.on()
        time.sleep(duration)
        self.off()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Cleanup GPIO settings on context exit.
        """
        GPIO.cleanup()
