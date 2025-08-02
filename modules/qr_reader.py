import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    timeout=1
)

def prompt_and_wait_for_qr() -> str:
    print("Waiting for QR code...")
    while(1):
        readData = ser.readline().decode('utf-8').strip()
        if readData:
            return readData

if __name__ == "__main__":
    scanned_data = prompt_and_wait_for_qr()
    print(f"Scanned QR code data: {scanned_data}")