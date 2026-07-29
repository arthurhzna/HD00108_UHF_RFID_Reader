from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DeviceStatusMessage:
    action: str
    id: str
    timestamp: str
    firmware_version: str