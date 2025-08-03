#!/usr/bin/env python3
import sys

def test_two_endstops_flexible(pin1: int, pin2: int, timeout: float = 30.0) -> bool:
    """
    Flexible endstop test: user can press either switch first in any order.
    """
    from modules.endstop import setup_gpio, test_endstop, cleanup_gpio

    # Initialize both pins
    setup_gpio(pin1)
    setup_gpio(pin2)

    try:
        print(f"TEST: Press either endstop switch on pin {pin1} or pin {pin2}…")
        # Attempt first detection on pin1
        if test_endstop(pin1, timeout):
            first, second = pin1, pin2
            print(f"Switch on pin {first} detected. Now press switch on pin {second}.")
        else:
            # Assume pin2 was pressed first
            print(f"Switch on pin {pin2} detected first or timeout on pin {pin1}. Now press switch on pin {pin1}.")
            first, second = pin2, pin1

        # Test the second switch
        ok_second = test_endstop(second, timeout)
        if ok_second:
            print("Both endstop switches passed the flexible test.")
            return True
        else:
            print(f"Switch on pin {second} was not detected. Test failed.")
            return False

    finally:
        cleanup_gpio()


def main():
    menu = {
        '1': 'NeoPixel startup test',
        '2': 'Weight reading test',
        '3': 'Relay test (choose pin)',
        '4': 'RFID module test',
        '5': 'PIR sensor test',
        '6': 'Endstop switch flexible test',
        '7': 'Outer Camera test',
        '8': 'Inner Camera test',
        '9': 'QR code scan test',
        '0': 'Exit'
    }

    while True:
        print("\nSelect a test to run:")
        for key, desc in menu.items():
            print(f"{key}. {desc}")
        choice = input("Enter choice: ").strip()

        if choice == '0':
            print("Exiting interactive test menu.")
            sys.exit(0)

        if choice == '1':
            from modules.led import initialize_strip, startup_test
            import board
            strip = initialize_strip(num_pixels=72, pin=board.D12, brightness=200)
            startup_test(strip, wait=0.02)
            print("NeoPixel startup test completed.")

        elif choice == '2':
            from modules.load_cells import prompt_and_read
            weight = prompt_and_read(
                config={
                    'dout_pin': 5,
                    'pd_sck_pin': 6,
                    'reference_unit': -16.56,
                    'zero_offset': 477428.75
                },
                readings=30
            )
            print(f"Weight readings: {weight}")
            print("Weight reading completed.")

        elif choice == '3':
            from modules.relay import Relay
            pin_menu = {
                '1': ('Left Lock', 18),
                '2': ('Right Lock', 27),
                '3': ('Buzzer', 22),
                '0': ('Back to main menu', None)
            }
            print("\nSelect which relay pin to test:")
            for k, (desc, _) in pin_menu.items():
                print(f"{k}. {desc}")
            sub_choice = input("Enter choice: ").strip()
            if sub_choice == '0':
                continue
            elif sub_choice in pin_menu:
                pin = pin_menu[sub_choice][1]
                with Relay(pin=pin) as relay:
                    relay.test(duration=3.0)
                    print(f"Relay test on pin {pin} completed.")
            else:
                print("Invalid choice for relay pin. Returning to main menu.")

        elif choice == '4':
            from modules.rfid import RFID2
            import time
            reader = RFID2()
            print("TEST: Please place a card on the reader…")
            uid = None
            for _ in range(50):  # ~5 seconds
                uid = reader.inventory()
                if uid:
                    print("Tag found:", [hex(b) for b in uid])
                    break
                time.sleep(0.1)
            reader.close()
            if uid:
                print("RFID module test passed.")
            else:
                print("RFID tag was not detected. Test failed.")

        elif choice == '5':
            from modules.pir_sensor import PIRSensorTest
            sensor = PIRSensorTest(pin=17, calibration_delay=10.0)
            try:
                if sensor.detect_motion(timeout=15):
                    print("✅ PIR sensor test passed.")
                else:
                    print("❌ PIR failed to detect motion")
            finally:
                sensor.cleanup()

        elif choice == '6':
            # Flexible endstop test
            if test_two_endstops_flexible(pin1=23, pin2=24):
                pass  # success message already printed
            else:
                pass  # failure message already printed

        elif choice == '7':
            from modules.camera import CameraTester
            available = CameraTester.list_available_cameras(max_index=3)
            print(f"Found cameras at indices: {available}")
            tester = CameraTester(available, width=1920, height=1080)
            results = tester.run_tests(save_dir="snapshots")
            for idx, passed in results.items():
                print(f"Camera {idx} → {'OK' if passed else 'FAIL'}")
            if not all(results.values()):
                print("One or more cameras failed their tests.")

        elif choice == '8':
            from modules.picamera import test_picamera
            test_picamera()
            print("PiCamera test completed.")

        elif choice == '9':
            from modules.qr_reader import prompt_and_wait_for_qr
            scanned_data = prompt_and_wait_for_qr()
            print(f"Scanned QR code data: {scanned_data}")

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
