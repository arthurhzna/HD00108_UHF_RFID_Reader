from __future__ import annotations

from config.serial import SerialConfig

from infrastructure.serial.serial_client import (
    SerialClient,
)


def build_serial_client(
    config: SerialConfig,
) -> SerialClient:

    return SerialClient(
        config=config,
    )