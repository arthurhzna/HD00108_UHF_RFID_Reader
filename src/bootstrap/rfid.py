from infrastructure.serial.serial_client import SerialClient

from infrastructure.rfid.uhf_rfid import (
    UHFRFID,
)


def build_uhf_rfid(
    serial: SerialClient,
) -> UHFRFID:
    rfid = UHFRFID(
        serial=serial,
    )

    rfid.set_rf_power_to_max()

    return rfid