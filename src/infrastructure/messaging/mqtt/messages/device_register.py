from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DeviceRegisterMessage:
    action: str
    id: str
    timestamp: str