# modules/rfid.py

import time
from mfrc522_i2c.mfrc522_i2c import MFRC522 as Reader

class RFID2:
    def __init__(self, bus_id=1, address=0x28):
        # Reader will open SMBus(bus_id) internally
        self.reader = Reader(bus_id, address)

    def inventory(self):
        """Returns the UID (list of bytes) or None if no tag."""
        scan_res = self.reader.scan()
        # scan_res is typically (status, uid_bytes_list)
        if scan_res and len(scan_res[1]) != 0:
            return scan_res[1]
        return None

    def close(self):
        # cleanly close the underlying SMBus
        self.reader.i2cBus.close()
