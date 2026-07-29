from domain.service.rfid import RFID


from infrastructure.rfid.command import (
    SET_RF_POWER_MAX_COMMAND,
    TAG_INVENTORY_COMMAND,
)

from infrastructure.rfid.parser import UHFRFIDParser
from infrastructure.serial.serial_client import SerialClient

class UHFRFID(RFID):

    def __init__(self, serial: SerialClient):
        self._serial = serial
        self._parser = UHFRFIDParser()

    def set_rf_power_to_max(self) -> bool:
        if not self._serial.write(SET_RF_POWER_MAX_COMMAND):
            return False

        response = self._serial.readline()

        return response is not None

    def inventory(self) -> list[str]:
        if not self._serial.write(TAG_INVENTORY_COMMAND):
            return []

        response = self._serial.read_bytes(
            512,
        )

        if response is None:
            return []

        return self._parser.inventory(response)