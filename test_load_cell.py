#!/usr/bin/env python3
"""
Test script to verify load cell readings and compare with calibration values.
"""

import sys
import time
from modules.load_cells import setup_scale, read_weight, cleanup

def test_load_cell():
    """Test load cell readings and display raw values for debugging."""
    
    print("Testing load cell readings...")
    print("=" * 50)
    
    # Initialize the scale
    hx = setup_scale()
    
    print(f"Current configuration:")
    print(f"  Reference unit: {hx.reference_unit}")
    print(f"  Zero offset: {hx.zero_offset}")
    print(f"  DOUT pin: 5")
    print(f"  SCK pin: 6")
    print()
    
    try:
        # Take multiple readings
        for i in range(5):
            print(f"Reading {i+1}:")
            
            # Get raw reading first
            from modules.load_cells import read_raw
            raw_value = read_raw(hx, readings=10)
            print(f"  Raw value: {raw_value:.2f}")
            
            # Get calculated weight
            weight = read_weight(hx, readings=10)
            print(f"  Calculated weight: {weight:.2f} grams")
            
            # Show the calculation
            calculated = (raw_value - hx.zero_offset) / hx.reference_unit
            print(f"  Manual calc: ({raw_value:.2f} - {hx.zero_offset}) / {hx.reference_unit} = {calculated:.2f}g")
            print()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        cleanup()
        print("GPIO cleanup completed")

if __name__ == "__main__":
    test_load_cell() 