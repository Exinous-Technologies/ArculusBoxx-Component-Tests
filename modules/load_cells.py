#!/usr/bin/env python3
"""
Module: hx711_module.py

Provides importable functions to initialize, read (with zero-offset and calibration), and clean up
readings from a single HX711 load cell amplifier connected to a Raspberry Pi.
Handles different HX711 library variants gracefully.
"""

import time
import RPi.GPIO as GPIO
from hx711 import HX711

__version__ = "1.4"

# Default HX711 configuration: BCM pin numbers, calibration factor, and zero offset
DEFAULT_CONFIG = {
    "dout_pin": 5,
    "pd_sck_pin": 6,
    "reference_unit": 2280,
    "zero_offset": 0,
}


def setup_scale(config=None):
    """
    Initialize GPIO and an HX711 instance with the given config.
    Attaches zero_offset and reference_unit values for downstream weight calculations.

    :param config: Dict with keys 'dout_pin', 'pd_sck_pin', 'reference_unit', 'zero_offset'.
                   If None, uses DEFAULT_CONFIG.
    :return: Initialized HX711 instance with attributes 'reference_unit' and 'zero_offset'.
    """
    if config is None:
        config = DEFAULT_CONFIG

    GPIO.setmode(GPIO.BCM)
    hx = HX711(dout_pin=config['dout_pin'], pd_sck_pin=config['pd_sck_pin'])

    # Attempt library-specific setup methods (format & scale) without affecting raw reads
    if hasattr(hx, 'set_reading_format'):
        try:
            hx.set_reading_format('MSB', 'MSB')
        except Exception:
            pass
    if hasattr(hx, 'set_reference_unit'):
        try:
            # we still call this so other library methods behave consistently
            hx.set_reference_unit(config['reference_unit'])
        except Exception:
            pass
    elif hasattr(hx, 'set_scale'):
        try:
            hx.set_scale(config['reference_unit'])
        except Exception:
            pass

    # Reset/tare if supported
    for method in ('reset', 'tare'):
        if hasattr(hx, method):
            try:
                getattr(hx, method)()
            except Exception:
                pass

    # Store calibration parameters for manual weight computation
    setattr(hx, 'reference_unit', config['reference_unit'])
    setattr(hx, 'zero_offset', config.get('zero_offset', 0))

    return hx


def _raw_read(hx):
    """
    Fallback raw read for HX711 variants.
    """
    if hasattr(hx, '_read'):
        return hx._read()
    raise AttributeError('No supported raw read method on HX711 object')


def read_weight(hx, readings=20):
    """
    Read an averaged weight measurement (in grams) from the provided HX711 instance,
    applying zero_offset and reference_unit.

    :param hx: HX711 instance returned by setup_scale
    :param readings: Number of raw samples to average
    :return: Weight in grams (float)
    """
    # Read raw counts, preferring bulk average if available
    # if hasattr(hx, 'read_average'):
    #     try:
    #         raw = hx.read_average(readings)
    #     except Exception:
    #         raw = sum(_raw_read(hx) for _ in range(readings)) / readings
    # else:
    #     values = []
    #     for _ in range(readings):
    #         if hasattr(hx, 'read'):
    #             val = hx.read(1)
    #         else:
    #             val = _raw_read(hx)
    #         values.append(val)
    #     raw = sum(values) / len(values)

    values = []
    for _ in range(readings):
        if hasattr(hx, 'read'):
            val = hx.read(1)
        else:
            val = _raw_read(hx)
        values.append(val)
        print(val)
    raw = sum(values) / len(values)

    # Apply offset and calibration factor
    weight = (raw - hx.zero_offset) / hx.reference_unit


    # Power cycle to save energy if supported
    if hasattr(hx, 'power_down'):
        try:
            hx.power_down()
        except Exception:
            pass
    time.sleep(0.1)
    if hasattr(hx, 'power_up'):
        try:
            hx.power_up()
        except Exception:
            pass

    return weight


def prompt_and_read(config=None, readings=5):
    """
    Prompt the user to place weight and press Enter, then return a single weight reading.

    :param config: Optional HX711 config dict including zero_offset and reference_unit
    :param readings: Number of samples to average
    :return: Weight reading in grams
    """
    hx = setup_scale(config)
    print(read_weight(hx, readings))
    input("Press Enter when a weight has been placed on the platform...")
    weight = read_weight(hx, readings)
    cleanup()
    return weight


def cleanup():
    """
    Clean up GPIO resources.
    """
    GPIO.cleanup()


# Expose only the public API
__all__ = [
    'setup_scale',
    'read_weight',
    'prompt_and_read',
    'cleanup',
    '__version__',
]
