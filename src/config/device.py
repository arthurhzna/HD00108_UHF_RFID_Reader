from __future__ import annotations

import os

from dataclasses import dataclass


@dataclass(slots=True)
class DeviceConfig:
    device_id: str
    software_version: str


def load_device_config() -> DeviceConfig:

    return DeviceConfig(
        device_id=os.getenv(
            "DEVICE_ID",
            "ini_rfid_scanner",
        ),
        software_version=os.getenv(
            "SOFTWARE_VERSION",
            "1.0.0",
        ),
    )