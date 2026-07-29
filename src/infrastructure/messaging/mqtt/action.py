from enum import StrEnum


class MQTTAction(StrEnum):
    DEVICE_REGISTER = "device_register"
    DEVICE_STATUS = "device_status"
    RFID_SUMMARY = "rfid_summary"