from __future__ import annotations

import os

from dataclasses import dataclass


@dataclass(slots=True)
class SerialConfig:
    port: str
    baudrate: int
    timeout: float
    reconnect: bool


def load_serial_config() -> SerialConfig:

    return SerialConfig(
        port=os.getenv(
            "SERIAL_PORT",
            "",
        ),

        baudrate=int(
            os.getenv(
                "SERIAL_BAUDRATE",
                "115200",
            )
        ),

        timeout=float(
            os.getenv(
                "SERIAL_TIMEOUT",
                "1.0",
            )
        ),

        reconnect=os.getenv(
            "SERIAL_RECONNECT",
            "true",
        ).lower() == "true",
    )