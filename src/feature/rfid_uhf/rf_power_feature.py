from externals.serial_client import SerialClient


class RfPowerFeature: 
    SET_MAX_POWER_ALL_ANTENNA = bytes([
        0x08,
        0xFF,
        0x2F,
        0x1E, 0x1E, 0x1E, 0x1E,
        0x37, 0x54
    ])
    def __init__(self, serial_client: SerialClient):
        self.serial_client = serial_client

    def set_all_rf_power_to_max(self):
        self.serial_client.write(self.SET_MAX_POWER_ALL_ANTENNA)
        data = self.serial_client.read_bytes(512)
        if data:
            return data
        else:
            return None