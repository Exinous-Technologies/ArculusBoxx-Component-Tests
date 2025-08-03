# Module for testing Raspberry Pi connected cameras.

import cv2
import os
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CameraTester:
    '''
    Helper class to test camera functionality.
    '''

    def __init__(self, camera_indices: List[int], width: int = 640, height: int = 480, timeout: int = 5):
        self.camera_indices = camera_indices
        self.width = width
        self.height = height
        self.timeout = timeout

    @staticmethod
    def list_available_cameras(max_index: int = 5) -> List[int]:
        '''
        Scans for available camera indices.
        '''
        available = []
        for idx in range(max_index + 1):
            cap = cv2.VideoCapture(idx)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            ret, frame = cap.read()
            cap.release()
            if ret:
                available.append(idx)
        return available

    def capture_frame(self, camera_index: int) -> Tuple[bool, any]:
        '''
        Captures a single frame from the given camera index.
        '''
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not cap.isOpened():
            logger.error(f'Camera {camera_index} could not be opened.')
            return False, None
        ret, frame = cap.read()
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
        del frame
        cap.release()
        if not ret or rotated_frame is None:
            logger.error(f'Failed to read frame from camera {camera_index}.')
            return False, None
        return True, rotated_frame

    def test_camera(self, camera_index: int, save_path: str = None) -> bool:
        '''
        Tests a single camera by capturing a frame and optionally saving it.
        Returns True if successful.
        '''
        success, frame = self.capture_frame(camera_index)
        if not success:
            return False
        if save_path:
            dirname = os.path.dirname(save_path)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            cv2.imwrite(save_path, frame)
            logger.info(f'Saved frame from camera {camera_index} to {save_path}')
        return True

    def run_tests(self, save_dir: str = None) -> Dict[int, bool]:
        '''
        Runs tests on all cameras and returns a dict of results.
        '''
        results = {}
        for idx in self.camera_indices:
            path = None
            if save_dir:
                filename = f'camera_{idx}.jpg'
                path = os.path.join(save_dir, filename)
            results[idx] = self.test_camera(idx, path)
        return results


def assert_camera_functional(camera_index: int, width: int = 640, height: int = 480):
    '''
    Assertion helper for test frameworks.
    '''
    tester = CameraTester([camera_index], width, height)
    ok = tester.test_camera(camera_index)
    assert ok, f'Camera {camera_index} failed test'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Test Raspberry Pi connected cameras.')
    parser.add_argument('--cameras', nargs='+', type=int, default=[0,1], help='List of camera indices to test')
    parser.add_argument('--width', type=int, default=640, help='Capture width')
    parser.add_argument('--height', type=int, default=480, help='Capture height')
    parser.add_argument('--save-dir', type=str, default=None, help='Directory to save captured images')
    args = parser.parse_args()
    tester = CameraTester(args.cameras, args.width, args.height)
    results = tester.run_tests(args.save_dir)
    for idx, ok in results.items():
        status = 'PASS' if ok else 'FAIL'
        print(f'Camera {idx}: {status}')
        if not ok:
            exit(1)
    exit(0)
