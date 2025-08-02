#!/usr/bin/env python3
import os
import glob
import time
from picamera2 import Picamera2

__all__ = ["test_picamera"]

def _find_picamera2():
    """
    Scan /dev/video* for a camera, and return a Picamera2 instance
    for the first device found (or None if none).
    """
    video_devs = sorted(glob.glob("/dev/video*"))
    if not video_devs:
        return None

    idx = int(os.path.basename(video_devs[0]).replace("video", ""))
    try:
        return Picamera2(camera_num=idx)
    except Exception:
        return None

def test_picamera(output_path: str = "./snapshots/picamera2.jpg") -> bool:
    """
    Capture a still image from the first Picamera2 device and save it.

    Args:
        output_path: full path (including filename) where the JPEG will be written.

    Returns:
        True if capture succeeded and file exists, False otherwise.
    """
    # Ensure directory exists
    snapshots_dir = os.path.dirname(output_path) or "."
    os.makedirs(snapshots_dir, exist_ok=True)

    # Find and initialize camera
    camera = _find_picamera2()
    if camera is None:
        print("❌ No Picamera2-compatible camera found.")
        return False

    # Configure for full‑res still capture
    config = camera.create_still_configuration()
    camera.configure(config)

    # Start camera, let auto‑exposure/whitebalance settle
    camera.start()
    time.sleep(2)

    # Capture and write
    try:
        camera.capture_file(output_path)
    except Exception as e:
        print(f"❌ Failed to capture image: {e}")
        camera.stop()
        return False

    camera.stop()

    if os.path.isfile(output_path):
        print(f"✅ Image saved to {output_path}")
        return True
    else:
        print("❌ Capture reported success, but file not found.")
        return False

if __name__ == "__main__":
    # If run as a script, use default path
    test_picamera()
