#!/usr/bin/env python3
"""
Standalone calibration script for HX711 load cell amplifier.
Determines and prints both the offset (zero reading) and the reference_unit (calibration factor) for converting raw counts to grams.
Takes 20 readings to compute the offset and 100 readings to compute the calibration factor.
"""

import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Configuration: BCM pin numbers for your HX711 wiring
DOUT_PIN = 5
SCK_PIN  = 6

# Number of samples to average for raw reading
def read_raw(hx, readings=10):
    values = []
    for _ in range(readings):
        if hasattr(hx, 'get_value'):
            val = hx.get_value(1)
        elif hasattr(hx, 'get_weight'):
            val = hx.get_weight(1)
        elif hasattr(hx, 'get_units'):
            val = hx.get_units(1)
        elif hasattr(hx, 'read_average'):
            val = hx.read_average(1)
        elif hasattr(hx, 'read'):
            val = hx.read(1)
        elif hasattr(hx, '_read'):
            val = hx._read()
        else:
            raise AttributeError('No supported read method on HX711')
        values.append(val)
    return sum(values) / len(values)


def main():
    print("Initializing HX711...")
    GPIO.setmode(GPIO.BCM)
    hx = HX711(DOUT_PIN, SCK_PIN)

    # Try library-specific setup methods gracefully
    if hasattr(hx, 'set_reading_format'):
        try:
            hx.set_reading_format('MSB', 'MSB')
        except Exception:
            pass
    # Use a unity scale to read raw values
    if hasattr(hx, 'set_reference_unit'):
        try:
            hx.set_reference_unit(1)
        except Exception:
            pass
    elif hasattr(hx, 'set_scale'):
        try:
            hx.set_scale(1)
        except Exception:
            pass

    # Reset and preliminary tare
    for method in ('reset', 'tare'):
        if hasattr(hx, method):
            try:
                getattr(hx, method)()
            except Exception:
                pass

    # Record offset (20 readings)
    input("Ensure the scale is empty and press Enter to record offset (20 readings)...")
    offset = read_raw(hx, readings=20)
    print(f"\nOffset (raw zero count): {offset:.2f}")

    # Ask for known weight
    known = float(input("\nPlace a known weight on the scale and enter its mass in grams: "))
    input("Press Enter when the weight is stable to take readings (100 readings)...")

    # Read raw count with weight (100 readings)
    raw_with_weight = read_raw(hx, readings=100)
    print(f"Raw reading with weight: {raw_with_weight:.2f}")

    # Compute calibration factor subtracting offset
    reference_unit = (raw_with_weight - offset) / known
    print(f"Suggested reference_unit (counts per gram): {reference_unit:.2f}\n")

    # Clean up GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()

