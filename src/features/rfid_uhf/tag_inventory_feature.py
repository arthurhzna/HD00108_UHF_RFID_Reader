from externals.serial_client import SerialClient

class TagInventoryFeature: 
    TAG_INVENTORY_COMMAND = bytes([0x09, 0xFF, 0x01, 0x04, 0x01, 0x00, 0x80, 0x0A, 0x3C, 0x48])
    def __init__(self, serial_client: SerialClient):
        self.serial_client = serial_client

    def get_tag_inventory(self):
        self.serial_client.write(self.TAG_INVENTORY_COMMAND)
        data = self.serial_client.read_bytes(512)
        if data:
            return data
        else:
            return None