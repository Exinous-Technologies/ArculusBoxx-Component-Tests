#!/usr/bin/env python3
"""
Script to calibrate load cell and update the load_cells.py module with correct values.
"""

import re
import subprocess
import sys

def run_calibration():
    """Run the calibration script and capture the output."""
    print("Running load cell calibration...")
    print("=" * 50)
    
    try:
        # Run the calibration script
        result = subprocess.run([sys.executable, 'loadcell_callibrate.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print("Calibration failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return None, None
            
        print(result.stdout)
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print("Calibration timed out!")
        return None, None
    except Exception as e:
        print(f"Error running calibration: {e}")
        return None, None

def extract_calibration_values(output):
    """Extract offset and reference_unit from calibration output."""
    if not output:
        return None, None
    
    # Look for the calibration values in the output
    offset_match = re.search(r'Offset \(raw zero count\): ([\d.-]+)', output)
    reference_match = re.search(r'Suggested reference_unit \(counts per gram\): ([\d.-]+)', output)
    
    if offset_match and reference_match:
        offset = float(offset_match.group(1))
        reference_unit = float(reference_match.group(1))
        return offset, reference_unit
    
    return None, None

def update_load_cells_module(offset, reference_unit):
    """Update the load_cells.py module with the new calibration values."""
    if offset is None or reference_unit is None:
        print("Cannot update module - missing calibration values")
        return False
    
    print(f"\nUpdating load_cells.py with new values:")
    print(f"  Zero offset: {offset}")
    print(f"  Reference unit: {reference_unit}")
    
    try:
        # Read the current file
        with open('modules/load_cells.py', 'r') as f:
            content = f.read()
        
        # Update the DEFAULT_CONFIG
        new_config = f'''# Default HX711 configuration: BCM pin numbers, calibration factor, and zero offset
DEFAULT_CONFIG = {{
    "dout_pin": 5,
    "pd_sck_pin": 6,
    "reference_unit": {reference_unit},
    "zero_offset": {offset},
}}'''
        
        # Replace the DEFAULT_CONFIG section
        pattern = r'# Default HX711 configuration: BCM pin numbers, calibration factor, and zero offset\s+DEFAULT_CONFIG = \{[^}]+\}'
        replacement = new_config
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write the updated file
        with open('modules/load_cells.py', 'w') as f:
            f.write(updated_content)
        
        print("Successfully updated load_cells.py!")
        return True
        
    except Exception as e:
        print(f"Error updating load_cells.py: {e}")
        return False

def main():
    """Main calibration and update process."""
    print("Load Cell Calibration and Module Update")
    print("=" * 50)
    
    # Run calibration
    stdout, stderr = run_calibration()
    
    if stdout is None:
        print("Calibration failed. Please check your setup and try again.")
        return
    
    # Extract values
    offset, reference_unit = extract_calibration_values(stdout)
    
    if offset is None or reference_unit is None:
        print("Could not extract calibration values from output.")
        print("Please run the calibration manually and note the values.")
        return
    
    # Update the module
    if update_load_cells_module(offset, reference_unit):
        print("\nCalibration complete! You can now use the load_cells module.")
        print("Run 'python test_load_cell.py' to verify the readings.")
    else:
        print("\nCalibration values extracted but module update failed.")
        print(f"Please manually update modules/load_cells.py with:")
        print(f"  reference_unit: {reference_unit}")
        print(f"  zero_offset: {offset}")

if __name__ == "__main__":
    main() 