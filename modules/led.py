# neopixel_startup.py

import time
import board
import neopixel

def initialize_strip(
    pin=board.D18,
    num_pixels: int = 72,
    brightness: float = 1,
    auto_write: bool = False
) -> neopixel.NeoPixel:
    """
    Return a configured NeoPixel strip object.
    
    Args:
        pin:        Data pin (e.g. board.D18).
        num_pixels: Number of LEDs in the strip.
        brightness: Global brightness (0.0 to 1.0).
        auto_write: If False, you must call .show() to update.
    """
    return neopixel.NeoPixel(pin, num_pixels, brightness=brightness, auto_write=auto_write)

def startup_test(strip: neopixel.NeoPixel, wait: float = 0.05) -> None:
    """
    Runs a colour wave on the strip: red, then green, then blue, then white.
    Each LED lights in sequence with the given delay.
    
    Args:
        strip: NeoPixel object returned by initialize_strip.
        wait:  Delay (in seconds) between each LED update.
    """
    # Define the sequence of colours
    colours = [
        (255, 0, 0),    # red
        (0, 255, 0),    # green
        (0, 0, 255),    # blue
        (255, 255, 255) # white
    ]
    
    for colour in colours:
        # wave this colour across the strip
        for i in range(len(strip)):
            strip.fill((0, 0, 0))   # clear previous
            strip[i] = colour
            strip.show()
            time.sleep(wait)
        # brief pause before next colour
        time.sleep(wait * 10)
    
    # turn everything off at the end
    strip.fill((0, 0, 0))
    strip.show()

if __name__ == "__main__":
    # Example usage when run as a script
    strip = initialize_strip()
    startup_test(strip)
