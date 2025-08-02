#!/usr/bin/env python3
"""
endstop_test.py

Test a mechanical endstop switch on a Raspberry Pi GPIO pin.

Usage (CLI):
    python endstop_test.py --pin 17 [--timeout 10]

Importable API:
    from endstop_test import setup_gpio, test_endstop, cleanup_gpio
    setup_gpio(pin)
    ok = test_endstop(pin, timeout=5)
    cleanup_gpio()
"""

import RPi.GPIO as GPIO
import argparse
import sys
import time

def setup_gpio(pin: int) -> None:
    """
    Initialize RPi.GPIO to use BCM numbering and set `pin` as input
    with an internal pull-up (so switch should pull it down to GND).
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup_gpio() -> None:
    """Restore GPIO to a safe state."""
    GPIO.cleanup()

def _wait_for(pin: int, target_state: int, timeout: float) -> bool:
    """
    Wait up to `timeout` seconds for GPIO.input(pin) == target_state.
    Returns True if seen, False on timeout.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if GPIO.input(pin) == target_state:
            return True
        time.sleep(0.01)
    return False

def test_endstop(pin: int, timeout: float = 30.0) -> bool:
    """
    Perform a full “press-and-release” test on the endstop.
    - Wait `timeout` s for a press (LOW)
    - Then wait `timeout` s for a release (HIGH)
    Returns True if both events succeed in time.
    """
    print(f"[Endstop Test] Pin {pin}: waiting up to {timeout}s for PRESS (LOW)...")
    if not _wait_for(pin, GPIO.LOW, timeout):
        print(f"[Endstop Test] Timeout waiting for press.")
        return False

    print(f"[Endstop Test] PRESS detected! Now waiting up to {timeout}s for RELEASE (HIGH)...")
    if not _wait_for(pin, GPIO.HIGH, timeout):
        print(f"[Endstop Test] Timeout waiting for release.")
        return False

    print(f"[Endstop Test] RELEASE detected! → PASS")
    return True

def main():
    parser = argparse.ArgumentParser(description="Mechanical endstop switch test")
    parser.add_argument(
        "--pin", "-p",
        type=int,
        required=True,
        help="BCM GPIO pin number where the switch is connected"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=30.0,
        help="Seconds to wait for each press/release event"
    )
    args = parser.parse_args()

    setup_gpio(args.pin)
    try:
        ok = test_endstop(args.pin, args.timeout)
        sys.exit(0 if ok else 1)
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    main()
